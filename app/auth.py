from fastapi import Header, HTTPException

API_KEYS = {"3c96b7e2-8e3a-4b10-a821-8d80b259f21e"}

def verify_token(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")