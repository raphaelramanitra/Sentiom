from fastapi import FastAPI
from routers import telemetry
from database import Base
# Important: We must import the model so SQLAlchemy registers it in Base.metadata 
# before calling create_all(), even if it appears unused in this file.
from models.database_models import SavedTelemetry
from database import engine


#Initalize database tables based on the defined models
Base.metadata.create_all(bind=engine)

#FastAPI application instance (centralizing routes)
app = FastAPI(title = "FastAPI Application", description = "This is a FastAPI application for IoT devices")

# Test route to check application status
@app.get("/")
def read_root():
    """Root endpoint to verify the API is running."""
    return {"message": "Sentiom IOT Application is online"}
    

app.include_router(telemetry.router)

# Launch uvicorn server when running the script directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)