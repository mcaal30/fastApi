from pydantic import BaseModel
from datetime import datetime
from typing import Optional

#1. Equema Base: Campos que comparten todos
class UserBase(BaseModel):
    name: str
    email: str #balida que tenga un formato de correo @

#2. Esquema pra crear(Request): Heeda de UserBase y pide la contrasena
class UserCreate(UserBase):
    password: str

#3.Essquema de Respuesta (response): Hereda de UserBase, agrega ID y fechas, pero no la contrase;a
class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None

#4. Esquema para actualizar: Campos opcionales para actualizar
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    #mejoras