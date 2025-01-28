import uvicorn
from fastapi import FastAPI, Depends

from app.database import init_db
from app.routes.instalaciones import router as Plants
from app.routes.notificaciones import router as Notification
from app.routes.usuarios import router as Users

# Initialize the database
init_db()

tags_metadata = [
    {
        "name": "Plants",
        "description": "Plants",
    },{
        "name": "Users",
        "description": "Users",
    },{
        "name": "Notification",
        "description": "Notification Server",
    }
]

app = FastAPI()

app.include_router(Plants, tags=["Plants"], prefix="/Plants")
app.include_router(Users, tags=["Users"], prefix="/Users")
app.include_router(Notification, tags=["Notification"], prefix="/Notification")