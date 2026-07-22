from pydantic import BaseModel, Field, StrictStr, field_validator, model_validator
from typing import Dict, Any
from datetime import datetime
from telemetry.devices_config import SUPPORTED_DEVICES

class IncomingTelemetry(BaseModel):
    """
    Pydantic schema for validating incoming telemetry payloads.
    Ensures all required fields are present, properly formatted, and within allowed values.
    """
    device_id: StrictStr = Field(..., description="Unique identifier for the device")
    device_type: StrictStr = Field(..., description="Type of the device")
    building_id: StrictStr = Field(..., description="Unique identifier for the building")
    unit: StrictStr = Field(..., description="Unit number inside a building")
    timestamp: datetime = Field(..., description="Timestamp of the data")
    values: Dict[str, Any] = Field(..., description="Dictionary containing sensor readings and their values")

    @field_validator("device_type")
    @classmethod
    def validate_device_type(cls, value:str) -> str:
        val_lower = value.lower()
        if val_lower not in SUPPORTED_DEVICES:
            raise ValueError(f"Invalid device type: {value} must be one of either {list(SUPPORTED_DEVICES.keys())}")
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
    
    @model_validator(mode='after')
    def validate_values_match_device_type(self) -> 'IncomingTelemetry':
        expected_schema = SUPPORTED_DEVICES.get(self.device_type, {})

        invalid_keys = [k for k in self.values.keys() if k not in expected_schema]
        if invalid_keys:
            raise ValueError(f"Invalid keys for device type '{self.device_type}': {invalid_keys}. Allowed: {list(expected_schema.keys())}")
        
        for key, expected_type in expected_schema.items():
            if key in self.values:
                val = self.values[key]
                if expected_type is int and isinstance(val, bool):
                    raise ValueError(f"Invalid type for '{key}': expected {expected_type.__name__}, got bool")
                
                if not isinstance(val, expected_type):
                    raise ValueError(f"Invalid type for '{key}': expected {expected_type}, got {type(val).__name__}")

        return self