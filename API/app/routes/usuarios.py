from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models import Usuarios, UserRequest, Instalaciones
from app.database import SessionLocal

router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create/", summary="Create new user")
async def create_notification(user_req: UserRequest, db: Session = Depends(get_db)):
    user = Usuarios(
        email=user_req.email,
        fullname=user_req.fullname,
        plant_id=user_req.plant_id,
        enabled=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"status": "User created", "user_id": user.id}

@router.get("/id/{user_id}", summary="Search user by id")
async def read_notification_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Usuarios).filter(Usuarios.id == user_id).first()
    if user is None:
        return {"error": "User not found"}
    return {
        "id": user.id,
        "email": user.email,
        "fullname": user.fullname,
        "plant_id": user.plant_id,
        "enabled": user.enabled,
        "created_at": user.created_at,
    }

@router.get("/listar", summary="Search all users")
async def read_notification_id(db: Session = Depends(get_db)):
    result = db.query(Usuarios, Instalaciones).join(Usuarios).filter(Instalaciones.id == Usuarios.plant_id).all()
    valores = []
    for usuarios, instalaciones in result:
        valores.append({
            "id": usuarios.id,
            "email": usuarios.email,
            "fullname": usuarios.fullname,
            "enabled": usuarios.enabled,
            "created_at": usuarios.created_at,
            "instalaciones": {
                "id": instalaciones.id,
                "name": instalaciones.name,
                "enabled": instalaciones.enabled,
                "created_at": instalaciones.created_at,
            }
        })
    return valores

@router.put("/disable/{user_id}", summary="Disable User by id")
async def read_notification_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Usuarios).filter(Usuarios.id == user_id).first()
    if user is None:
        return {"error": "User not found"}
    user.enabled = False
    db.commit()
    return {"status": "Disable User", "user_id": user.id}

@router.delete("/{user_id}", summary="delete user by id")
async def delete_notification(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Usuarios).filter(Usuarios.id == user_id).first()
    db.delete(user)
    if user is None:
        return {"error": "User not found"}
    
    db.commit()
    return {"status": "User delete", "user_id": user.id}