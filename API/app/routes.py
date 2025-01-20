from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models import Notification, NotificationRequest
from app.database import SessionLocal

router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create/", summary="Create new notification")
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

@router.get("/id/{notification_id}", summary="Search notifications by id")
async def read_notification_id(notification_id: int, db: Session = Depends(get_db)):
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

@router.get("/recipient/{notification_recipient}", summary="Search notifications by recipient")
async def read_notification_recipient(notification_recipient: str, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.recipient == notification_recipient).all()
    if notification is None:
        return {"error": "Notification not found"}
    valores = []
    for row in notification:
        valores.append({
        "id": row.id,
        "recipient": row.recipient,
        "message": row.message,
        "status": row.status,
        "created_at": row.created_at,
        })
    return valores

@router.get("/status/{notification_status}", summary="Search notifications by status")
async def read_notification_status(notification_status: str, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.status == notification_status).all()
    if notification is None:
        return {"error": "Notification not found"}
    valores = []
    for row in notification:
        valores.append({
        "id": row.id,
        "recipient": row.recipient,
        "message": row.message,
        "status": row.status,
        "created_at": row.created_at,
        })
    return valores

@router.put("/{notification_id}", summary="Update notifications by id")
async def update_notification_status(notification_id: int, status: str, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification is None:
        return {"error": "Notification not found"}
    
    notification.status = status
    db.commit()
    return {"status": "Notification updated", "notification_id": notification.id}

@router.delete("/{notification_id}", summary="delete notifications by id")
async def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    db.delete(notification)
    if notification is None:
        return {"error": "Notification not found"}
    
    db.commit()
    return {"status": "Notification updated", "notification_id": notification.id}