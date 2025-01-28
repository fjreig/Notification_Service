from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models import Instalaciones, PlantRequest
from app.database import SessionLocal

router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create/", summary="Create new plant")
async def create_notification(plant_req: PlantRequest, db: Session = Depends(get_db)):
    plant = Instalaciones(
        name=plant_req.name,
        enabled=True,
    )
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return {"status": "Plant created", "plant_id": plant.id}

@router.get("/id/{plant_id}", summary="Search plant by id")
async def read_notification_id(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Instalaciones).filter(Instalaciones.id == plant_id).first()
    if plant is None:
        return {"error": "Plant not found"}
    return {
        "id": plant.id,
        "name": plant.name,
        "enabled": plant.enabled,
        "created_at": plant.created_at,
    }

@router.get("/listar", summary="Search all plants")
async def read_notification_id(db: Session = Depends(get_db)):
    plant = db.query(Instalaciones).all()
    if plant is None:
        return {"error": "Plant not found"}
    valores = []
    for row in plant:
        valores.append({
            "id": row.id,
            "name": row.name,
            "enabled": row.enabled,
            "created_at": row.created_at,
        })
    return valores

@router.put("/disable/{plant_id}", summary="Disable plants by id")
async def read_notification_id(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Instalaciones).filter(Instalaciones.id == plant_id).first()
    if plant is None:
        return {"error": "Plant not found"}
    plant.enabled = False
    db.commit()
    return {"status": "Disable plant", "plant_id": plant.id}

@router.delete("/{plant_id}", summary="delete plant by id")
async def delete_notification(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Instalaciones).filter(Instalaciones.id == plant_id).first()
    db.delete(plant)
    if plant is None:
        return {"error": "Plant not found"}
    
    db.commit()
    return {"status": "Plant delete", "plant_id": plant.id}