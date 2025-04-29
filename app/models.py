from sqlalchemy import Column, Integer, Float, String, Boolean, BigInteger
from .database import Base

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    timestamp = Column(BigInteger)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Integer)
    direction = Column(Float)
    ignition_on = Column(Boolean)
    gps_fixed = Column(Boolean)