# IoT Telemetry API

A robust, lightweight API built with **FastAPI** to ingest, validate, and analyze telemetry data from various IoT sensors. The system evaluates incoming data against business rules to detect anomalies in real-time and persists the payloads into a database.

## 📁 Project Structure

The codebase follows a modular architecture to separate concerns and ensure maintainability:

```text
├── main.py                 # FastAPI application entry point
├── database/               # Database domain
│   ├── database.py         # Connection and session management
│   └── models.py           # SQLAlchemy database schema
├── telemetry/              # Telemetry domain
│   ├── router.py           # API endpoints (/telemetry)
│   └── schemas.py          # Pydantic data validation
├── services/               # Shared business logic
│   └── anomaly_engine.py   # Core anomaly threshold rules
└── tests/                  # Automated test suite
    └── test_api.py
    └── test_anomaly_engine.py
```
