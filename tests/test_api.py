from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ingestion_and_validation():
    # Validate ingestion of telemetry data as well as validation and persistence
    payload = {
        "device_id": "TEST-001",
        "device_type": "kepler",
        "building_id": "MVTCC",
        "unit": "101",
        "timestamp": "2026-07-21T18:00:00Z",
        "values": {
            "temperature_c": 22.5,
            "humidity_pct": 45.0,
            "leak_resistance_ohm": 200000,
            "battery_pct": 90,
            "signal_quality": -50
        }
    }

    response = client.post("/telemetry", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "saved_id" in data

def test_query_behavior_anomalies():
    """Valide le comportement de la requête GET pour les anomalies."""
    # Validate the GET endpoint for anomalies returns the expected results
    bad_payload = {
        "device_id": "TEST-002",
        "device_type": "kepler",
        "building_id": "MVTCC",
        "unit": "101",
        "timestamp": "2026-07-21T18:05:00Z",
        "values": {
            "temperature_c": 1.5, # Activates rule A-002
            "battery_pct": 100,
            "leak_resistance_ohm": 200000,
            "signal_quality": -50
        }
    }
    client.post("/telemetry/", json=bad_payload)
    
    response = client.get("/telemetry/anomalies")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_anomalies_found"] >= 1
    
    first_anomaly = data["data"][0]
    assert "anomalies" in first_anomaly
    assert len(first_anomaly["anomalies"]) > 0