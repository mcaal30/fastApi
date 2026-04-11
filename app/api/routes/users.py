# Archivo: app/api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.models.user import User # Importamos el modelo ORM

router = APIRouter()

@router.post("/", response_model=UserResponse) #decorador @ filtra los datos no deja pasar las contraseña de vuelta como respuesta json
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el email ya existe
    usuario_existente = db.query(User).filter(User.email == user_in.email).first() #Es la condición. Le dice: "Busca donde la columna 'email' de la tabla sea exactamente igual al correo que el usuario acaba de enviar". primer resutlado que encuentre
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
    db.commit() #traducción a codigo sql
    db.refresh(nuevo_usuario) # Refresca el objeto para obtener el ID generado

    return nuevo_usuario

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    # Trae todos los usuarios de la base de datos
    usuarios = db.query(User).all()
    return usuarios

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    # Buscar el usuario por ID
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar campos si se proporcionan
    if user_update.name is not None:
        usuario.name = user_update.name
    if user_update.email is not None:
        # Verificar si el email ya existe en otro usuario
        email_existente = db.query(User).filter(User.email == user_update.email, User.id != user_id).first()
        if email_existente:
            raise HTTPException(status_code=400, detail="El email ya está registrado por otro usuario")
        usuario.email = user_update.email
    if user_update.password is not None:
        usuario.password = hashlib.sha256(user_update.password.encode()).hexdigest()
    
    # Guardar cambios
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Buscar el usuario por ID
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Eliminar el usuario
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}

#mejoras