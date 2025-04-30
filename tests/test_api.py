from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models import LocationResponse

client = TestClient(app)

valid_token = "3c96b7e2-8e3a-4b10-a821-8d80b259f21e"
device_id = "0A3F73000000"

def test_missing_api_key():
    response = client.get(f"/api/v1/location/{device_id}")
    assert response.status_code == 422

def test_invalid_api_key():
    response = client.get(f"/api/v1/location/{device_id}", headers={"x-api-key": "invalid"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API Key"}

def test_device_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None

    with patch("app.main.SessionLocal", return_value=mock_session):
        response = client.get("/api/v1/location/UNKNOWN_ID", headers={"x-api-key": valid_token})
        assert response.status_code == 404
        assert response.json() == {"detail": "Device not found"}

def test_successful_location_response():
    mock_location = LocationResponse(
        device_id=device_id,
        timestamp=1714501234,
        latitude=-21.01,
        longitude=-42.53,
        speed=60,
        direction=54.87,
        ignition_on=True,
        gps_fixed=True
    )

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_location

    with patch("app.main.SessionLocal", return_value=mock_session):
        response = client.get(f"/api/v1/location/{device_id}", headers={"x-api-key": valid_token})
        assert response.status_code == 200
        assert response.json() == mock_location.dict()
