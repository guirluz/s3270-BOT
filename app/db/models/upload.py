"""
upload.py

Modelo SQLAlchemy que representa los archivos subidos (Excel).
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class Upload(Base):
    """
    Representa un archivo subido al sistema.
    """

    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(
        String(255),
        nullable=False,
        comment="Nombre original del archivo"
    )

    status = Column(
        String(50),
        nullable=False,
        default="pending",
        comment="Estado del procesamiento"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Fecha de creación"
    )

