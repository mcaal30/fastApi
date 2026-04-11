# Archivo: app/api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User # Importamos el modelo ORM

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el email ya existe
    usuario_existente = db.query(User).filter(User.email == user_in.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # 2. Encriptar contraseña
    hashed_password = hashlib.sha256(user_in.password.encode()).hexdigest()

    # 3. Crear el objeto en Python (Instancia del modelo)
    nuevo_usuario = User(
        name=user_in.name,
        email=user_in.email,
        password=hashed_password
    )

    # 4. Guardar en la base de datos a través del ORM
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario) # Refresca el objeto para obtener el ID generado

    return nuevo_usuario

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    # Trae todos los usuarios de la base de datos
    usuarios = db.query(User).all()
    return usuarios