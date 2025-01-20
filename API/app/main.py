import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import Notification
from app.database import SessionLocal, init_db

app = FastAPI()

# Initialize the database
init_db()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request validation
class NotificationRequest(BaseModel):
    recipient: str
    message: str

@app.post("/notifications/")
async def create_notification(notification_req: NotificationRequest, db: Session = Depends(get_db)):
    notification = Notification(
        recipient=notification_req.recipient,
        message=notification_req.message,
        status="pending",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return {"status": "Notification created", "notification_id": notification.id}

@app.get("/notifications/{notification_id}")
async def read_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification is None:
        return {"error": "Notification not found"}
    return {
        "id": notification.id,
        "recipient": notification.recipient,
        "message": notification.message,
        "status": notification.status,
        "created_at": notification.created_at,
    }

@app.put("/notifications/{notification_id}")
async def update_notification_status(notification_id: int, status: str, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification is None:
        return {"error": "Notification not found"}
    
    notification.status = status
    db.commit()
    return {"status": "Notification updated", "notification_id": notification.id}