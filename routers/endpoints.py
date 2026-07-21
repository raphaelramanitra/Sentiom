from fastapi import APIRouter, Depends
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
        temperature_c=payload.values["temperature_c"],
        humidity_pct=payload.values["humidity_pct"],
        leak_resistance_ohm=payload.values["leak_resistance_ohm"],
        battery_pct=payload.values["battery_pct"],
        signal_quality=payload.values["signal_quality"]
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {
        "status": "success",
        "message": "Telemetry data saved to database successfully",
        "saved_id": db_item.id
    }