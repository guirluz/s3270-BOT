"""
task_repository.py

Capa de persistencia para el estado de tareas Celery.
"""

from sqlalchemy.orm import Session
from app.db.models.task import TaskExecution


def create_task(
    db: Session,
    task_id: str,
    task_type: str,
    status: str,
):
    task = TaskExecution(
        task_id=task_id,
        task_type=task_type,
        status=status,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(
    db: Session,
    task_id: str,
    status: str,
    result: str | None = None,
    error: str | None = None,
):
    task = db.query(TaskExecution).filter_by(task_id=task_id).first()
    if not task:
        return None

    task.status = status
    task.result = result
    task.error = error
    db.commit()
    return task