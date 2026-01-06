"""
bot_tasks.py

Define tareas asíncronas ejecutadas por Celery.

Responsabilidades:
- Ejecutar procesos largos del bot 3270
- Reportar estado y progreso
- Retornar resultados estructurados

Este módulo NO depende de FastAPI.
Tareas Celery con persistencia real en PostgreSQL.
"""

import time
from celery import shared_task

from app.db.session import SessionLocal
from app.db.models.task import TaskExecution


@shared_task(bind=True)
def login_bot_task(self, username: str, password: str) -> dict:
    """
    Tarea asíncrona de login 3270 con persistencia en DB.
    """

    db = SessionLocal()

    try:
        # ----------------------------------
        # Marcar RUNNING
        # ----------------------------------
        task = db.query(TaskExecution).filter(
            TaskExecution.task_id == self.request.id
        ).first()

        if task:
            task.status = "RUNNING"
            db.commit()

        # Simular conexión
        time.sleep(2)

        if not username or not password:
            raise ValueError("Username and password required")

        time.sleep(2)

        if username != "admin" or password != "admin":
            result = {"status": "FAILED", "message": "Invalid credentials"}

            if task:
                task.status = "FAILED"
                task.error = "Invalid credentials"
                db.commit()

            return result

        time.sleep(2)

        result = {
            "status": "SUCCESS",
            "message": "Login successful",
            "screen": "MAIN MENU"
        }

        if task:
            task.status = "DONE"
            task.result = str(result)
            db.commit()

        return result

    except Exception as exc:
        if task:
            task.status = "FAILED"
            task.error = str(exc)
            db.commit()
        raise

    finally:
        db.close()
