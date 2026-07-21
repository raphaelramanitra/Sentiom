from datetime import datetime, timezone
import json
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models.telemetry import IncomingTelemetry
from models.database_models import SavedTelemetry
from database import get_db, engine
from services.anomaly_engine import detect_anomalies

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

@router.post("/")
def receive_telemetry(payload: IncomingTelemetry, db: Session = Depends(get_db)):


    anomalies = detect_anomalies(payload.device_type, payload.values)

    enriched_values = payload.values.copy()
    enriched_values["_metadata"] = {
        "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
        "processing_status": "processed",
        "anomalies_detected": len(anomalies) > 0,
        "anomalies": anomalies
    }

    db_item = SavedTelemetry(
        device_id=payload.device_id,
        device_type=payload.device_type,
        building_id=payload.building_id,
        unit=payload.unit,
        timestamp=payload.timestamp,
        values = enriched_values
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {
        "status": "success",
        "message": "Telemetry data saved to database successfully",
        "saved_id": db_item.id
    }

@router.get("/")
def get_telemetry(
    device_id: Optional[str] = Query(None, description="Filter by device ID (ex: KP-1023)"),
    device_type: Optional[str] = Query(None, description="Filter by device type (ex: kepler, archimede, newton, galileo, thermostat)"),
    building_id: Optional[str] = Query(None, description="Filter by building ID (ex: BLDG-001)"),
    unit: Optional[str] = Query(None, description="Filter by unit number (ex: 101)"),

    limit: int = Query(20, description="Maximum number of results to return"),
    db: Session = Depends(get_db)
):
    query = db.query(SavedTelemetry)
    if device_type:
        query = query.filter(SavedTelemetry.device_type == device_type)
    if device_id:
        query = query.filter(SavedTelemetry.device_id == device_id)
    if building_id:
        query = query.filter(SavedTelemetry.building_id == building_id)
    if unit:
        query = query.filter(SavedTelemetry.unit == unit)
        
    results = query.order_by(SavedTelemetry.id.desc()).limit(limit).all()
    
    return {
        "total_results": len(results),
        "data": results
    }

@router.get("/anomalies")
def get_active_anomalies(
    device_id: Optional[str] = Query(None, description="Filter by device ID (ex: KP-1023)"),
    building_id: Optional[str] = Query(None, description="Filter by building ID (ex: MVTCC)"),
    severity: Optional[str] = Query(None, description="Filter by severity (ex: Critique, Moyenne)"),
    limit: int = Query(20, description="Maximum number of results to return"),
    db: Session = Depends(get_db)

):
    query = db.query(SavedTelemetry)
    if device_id:
        query = query.filter(SavedTelemetry.device_id == device_id)
    if building_id:
        query = query.filter(SavedTelemetry.building_id == building_id)
        
    results = query.order_by(SavedTelemetry.id.desc()).all()
    
    anomalies_list = []
    for row in results: 
        values_dict = row.values if isinstance(row.values, dict) else json.loads(row.values)
        metadata = values_dict.get("_metadata", {})

        if metadata.get("anomalies_detected"):
            active_anomalies = metadata.get("anomalies", [])
            
            anomalies_list.append({
                "id": row.id,
                "device_id": row.device_id,
                "building_id": row.building_id,
                "timestamp": row.timestamp,
                "ingestion_timestamp": metadata.get("ingestion_timestamp"),
                "anomalies": active_anomalies
            })

            if len(anomalies_list) >= limit:
                break

    return {
        "total_anomalies_found": len(anomalies_list),
        "data": anomalies_list
    }