# Archivo: app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import users

# --- IMPORTACIONES NUEVAS ---
from app.db.database import engine, Base
from app.models import user # Importamos para que SQLAlchemy detecte el modelo

# EL TOQUE MÁGICO: Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)
# ----------------------------

app = FastAPI(title="API con ORM")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/usuarios", tags=["Usuarios"])