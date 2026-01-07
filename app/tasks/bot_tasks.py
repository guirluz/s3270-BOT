"""
bot_tasks.py

Define tareas asíncronas ejecutadas por Celery.

Responsabilidades:
- Ejecutar procesos largos del bot 3270
- Actualizar estado en PostgreSQL
- Retornar resultados estructurados

Este módulo NO depende de FastAPI.
"""

import time
from app.celery_app import celery_app
from app.db.session import SessionLocal
from app.tasks.task_repository import update_task


@celery_app.task(bind=True, name="login_bot_task")
def login_bot_task(self, username: str, password: str) -> dict:
    """
    Tarea asíncrona de login 3270 con Redis + PostgreSQL.
    """

    db = SessionLocal()

    try:
        update_task(
            db=db,
            task_id=self.request.id,
            status="RUNNING"
        )

        time.sleep(2)

        if not username or not password:
            raise ValueError("Username and password required")

        time.sleep(2)

        if username != "admin" or password != "admin":
            update_task(
                db=db,
                task_id=self.request.id,
                status="FAILED",
                error="Invalid credentials"
            )
            return {
                "status": "FAILED",
                "message": "Invalid credentials"
            }

        time.sleep(2)

        result = {
            "status": "SUCCESS",
            "message": "Login successful",
            "screen": "MAIN MENU"
        }

        update_task(
            db=db,
            task_id=self.request.id,
            status="DONE",
            result=str(result)
        )

        return result

    except Exception as exc:
        update_task(
            db=db,
            task_id=self.request.id,
            status="FAILED",
            error=str(exc)
        )
        raise

    finally:
        db.close()