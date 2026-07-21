from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime

class IncomingTelemetry(BaseModel):
    device_id: str = Field(..., description="Unique identifier for the device")
    device_type: str = Field(..., description="Type of the device")
    building_id: str = Field(..., description="Unique identifier for the building")
    unit: str = Field(..., description="Unit number inside a building")
    timestamp: datetime = Field(..., description="Timestamp of the data")
    values: Dict[str, Any] = Field(..., description="Dictionary containing sensor readings and their values")