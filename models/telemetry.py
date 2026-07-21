from pydantic import BaseModel, Field, StrictStr, field_validator
from typing import Dict, Any
from datetime import datetime

class IncomingTelemetry(BaseModel):
    device_id: StrictStr = Field(..., description="Unique identifier for the device")
    device_type: StrictStr = Field(..., description="Type of the device")
    building_id: StrictStr = Field(..., description="Unique identifier for the building")
    unit: StrictStr = Field(..., description="Unit number inside a building")
    timestamp: datetime = Field(..., description="Timestamp of the data")
    values: Dict[str, Any] = Field(..., description="Dictionary containing sensor readings and their values")

    @field_validator("device_type")
    @classmethod
    def validate_device_type(cls, value:str) -> str:
        allowed_types = ["kepler", "archimede", "newton", "galileo", "thermostat"]
        val_lower = value.lower()
        if val_lower not in allowed_types:
            raise ValueError(f"Invalid device type: {value} must be one of either {allowed_types}")
        return val_lower
    
    @field_validator("building_id", "unit", "device_id")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("This entry cannot be empty or whitespace.")
        return value.strip()
    
    @field_validator("values")
    @classmethod
    def validate_values_not_empty(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        if not value:
            raise ValueError("The 'values' dictionary cannot be empty.")
        return value