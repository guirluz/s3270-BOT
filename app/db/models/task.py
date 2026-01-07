from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class TaskExecution(Base):
    __tablename__ = "task_executions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    task_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    task_type = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    result = Column(
        Text,
        nullable=True
    )

    error = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

