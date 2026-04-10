# Archivo: app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión postgresql
SQLALCHEMY_DATABASE_URL = "postgresql://postgres@localhost/User"

# 1. El Engine es el motor que maneja la comunicación con la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=5, max_overflow=10)

# 2. SessionLocal es la fábrica de sesiones para nuestras rutas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base es la clase de la que heredarán todos nuestros modelos
Base = declarative_base()

# 4. Inyección de dependencias para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()