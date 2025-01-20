import uvicorn
from fastapi import FastAPI, Depends

from app.database import init_db
from app.routes import router as Notification

# Initialize the database
init_db()

tags_metadata = [
    {
        "name": "Notification",
        "description": "Notification Server",
    }
]

app = FastAPI()

app.include_router(Notification, tags=["Notification"], prefix="/Notification")
