from fastapi import APIRouter
from models.telemetry import IncomingTelemetry

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

@router.post("/")
def receive_telemetry(payload: IncomingTelemetry):
    return {
        "status": "success",
        "message": "Telemetry data received successfully",
        "data": payload
    }