from sqlalchemy import Column, Float, Integer, String, DateTime
from database import Base

class SavedTelemetry(Base):
    __tablename__ = "telemetry_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(String, index=True)
    device_type = Column(String)
    building_id = Column(String)
    unit = Column(String)
    timestamp = Column(DateTime)
    temperature_c = Column(Float)
    humidity_pct = Column(Float)
    leak_resistance_ohm = Column(Float)
    battery_pct = Column(Integer)
    signal_quality = Column(Float)