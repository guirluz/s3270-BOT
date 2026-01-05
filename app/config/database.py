"""
database.py

Configura la conexión a PostgreSQL usando SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings


# Crear el engine (conexión base)
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Detecta conexiones muertas
)


# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Dependencia para obtener una sesión de base de datos.

    Se usa en FastAPI con Depends().
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
