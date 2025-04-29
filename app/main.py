from fastapi import FastAPI
from .database import SessionLocal
from .models import Location

app = FastAPI()

@app.get("/api/v1/location/{device_id}")
def get_device_location(device_id: str):
    db = SessionLocal()
    location = db.query(Location).filter(Location.device_id == device_id).first()
    db.close()

    if location:
        return {
            "device_id": location.device_id,
            "timestamp": location.timestamp,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "speed": location.speed,
            "direction": location.direction,
            "ignition_on": location.ignition_on,
            "gps_fixed": location.gps_fixed
        }
    else:
        return {"error": "Device not found"}
    
    
    
    