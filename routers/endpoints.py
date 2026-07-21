from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models.telemetry import IncomingTelemetry
from models.database_models import SavedTelemetry
from database import get_db, engine

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

@router.post("/")
def receive_telemetry(payload: IncomingTelemetry, db: Session = Depends(get_db)):

    print(f"DEBUG - URL de la BD active : {engine.url}")

    db_item = SavedTelemetry(
        device_id=payload.device_id,
        device_type=payload.device_type,
        building_id=payload.building_id,
        unit=payload.unit,
        timestamp=payload.timestamp,
        values = payload.values
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
def get_telemetry_history(
    device_id: Optional[str] = Query(None, description="Filtrer par ID d'appareil (ex: KP-1023)"),
    limit: int = Query(10, description="Nombre maximum de résultats à retourner"),
    db: Session = Depends(get_db)
):
    query = db.query(SavedTelemetry)
    if device_id:
        query = query.filter(SavedTelemetry.device_id == device_id)
        
    results = query.order_by(SavedTelemetry.id.desc()).limit(limit).all()
    
    return {
        "total_results": len(results),
        "data": results
    }