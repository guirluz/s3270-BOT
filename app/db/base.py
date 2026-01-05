"""
base.py

Define la Base declarativa de SQLAlchemy.
Todas las tablas heredan de aquí.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Clase base para todos los modelos ORM.
    """
    pass
