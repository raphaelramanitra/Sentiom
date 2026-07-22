# IoT Telemetry API

A lightweight API built with **FastAPI** to ingest, validate, and analyze telemetry data from various IoT sensors. The system evaluates incoming data against business rules to detect anomalies in real-time and persists the payloads into a database.

## 📁 Project Structure

The codebase follows a modular architecture to separate concerns and ensure maintainability:

```text
├── main.py                 # FastAPI application entry point
├── database/               # Database domain
│   ├── database.py         # Connection and session management
│   └── models.py           # SQLAlchemy database schema
├── telemetry/              # Telemetry domain
│   ├── router.py           # API endpoints (/telemetry)
│   ├── schemas.py          # Pydantic data validation
│   └── devices_config.py   # Device types and allowed fields/types config
├── services/               # Shared business logic
│   └── anomaly_engine.py   # Core anomaly threshold rules
├── tests/                  # Automated test suite
│   ├── test_api.py
│   └── test_anomaly_engine.py
├── Étude de cas - Sentiom.pdf

```

## Prerequisites & Installation

```text
Make sure python is installed as well as all dependencies (FastAPI, Uvicorn, Pydantic, SQLAlchemy, Pytest, etc):

py -m pip install fastapi uvicorn sqlalchemy pydantic pytest httpx

```

## Running the Project

```text
Start the Uvicorn Server from the root of the project:

py -m uvicorn main:app --reload
```

## Running Tests

```text
To run the automated test suite (unit and integration tests via pytest) :
py -m pytest
```
