from fastapi import FastAPI
from routers import endpoints
from database import Base
from models.database_models import SavedTelemetry
from database import engine


#Initalize database tables based on the defined models
Base.metadata.create_all(bind=engine)

#FastAPI application instance (centralizing routes)
app = FastAPI(title = "FastAPI Application", description = "This is a FastAPI application for IoT devices")

#test route to check application status
@app.get("/")
def read_root():
    return {"message": "Sentiom IOT Application is online"}
    

app.include_router(endpoints.router)

#launch uvicorn server when running the app locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)