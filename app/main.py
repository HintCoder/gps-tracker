from fastapi import FastAPI, Depends, HTTPException
from .database import SessionLocal
from .models import Location, LocationResponse
from .auth import verify_token

app = FastAPI()

@app.get("/api/v1/location/{device_id}", response_model=LocationResponse)
def get_device_location(device_id: str, token: str = Depends(verify_token)):
    db = SessionLocal()
    location = db.query(Location).filter(Location.device_id == device_id).first()
    db.close()

    if location:
        return location
    else:
        raise HTTPException(status_code=404, detail="Device not found")
    
    
    
    