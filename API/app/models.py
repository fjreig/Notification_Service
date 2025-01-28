from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()

class Instalaciones(Base):
    __tablename__ = "instalaciones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    enabled = Column(Boolean, default=True)

class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("instalaciones.id"))
    email = Column(String, index=True)
    fullname = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    enabled = Column(Boolean, default=True)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("instalaciones.id"))
    message = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime)
    enabled = Column(Boolean, default=True)


class PlantRequest(BaseModel):
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                'name' : "Plant 1"
            }
        }

class UserRequest(BaseModel):
    email: str
    fullname: str
    plant_id: int

    class Config:
        json_schema_extra = {
            "example": {
                'plant_id' : 1,
                'fullname' : "Operator Full",
                'email' : "user1@info.com",
            }
        }

class NotificationRequest(BaseModel):
    message: str
    plant_id: int

    class Config:
        json_schema_extra = {
            "example": {
                'plant_id' : 1,
                'message' : "Alarm 1",
            }
        }