"""
init_db.py

Crea todas las tablas en la base de datos.
"""

from app.db.session import engine
from app.db.base import Base

# Importar modelos para que SQLAlchemy los registre
from app.db.models.upload import Upload
from app.db.models.record import Record
from app.db.models.log import ProcessingLog
from app.db.models.task import TaskExecution


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
