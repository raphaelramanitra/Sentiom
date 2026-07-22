from sqlalchemy import JSON, Column, Float, Integer, String, DateTime
from database.database import Base

class SavedTelemetry(Base):
    """
    SQLAlchemy model representing the 'telemetry_data' table in the database.
    Stores ingested telemetry payloads along with their processed metadata and anomalies.
    """
    __tablename__ = "telemetry_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(String, index=True)
    device_type = Column(String)
    building_id = Column(String)
    unit = Column(String)
    timestamp = Column(DateTime)
    # Uses JSON to store the flexible 'values' dictionary, including the added '_metadata'
    values = Column(JSON)