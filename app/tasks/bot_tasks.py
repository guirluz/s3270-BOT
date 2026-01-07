"""
bot_tasks.py

Define tareas asíncronas ejecutadas por Celery.

Responsabilidades:
- Ejecutar procesos largos del bot 3270
- Orquestar Flow + Session
- Actualizar estado en PostgreSQL
- Retornar resultados estructurados

Este módulo NO depende de FastAPI.
"""

from app.celery_app import celery_app
from app.db.session import SessionLocal
from app.tasks.task_repository import update_task

from app.bot.session import Socket3270Session
from app.bot.flow.login_flow import LoginFlow
from app.bot.screen.screen_matcher import ScreenMatcher


@celery_app.task(bind=True, name="login_bot_task")
def login_bot_task(self, username: str, password: str) -> dict:
    """
    Tarea asíncrona que ejecuta el flujo real de login 3270.
    """

    db = SessionLocal()
    session = None

    try:
        # ------------------------------
        # Marcar RUNNING
        # ------------------------------
        update_task(
            db=db,
            task_id=self.request.id,
            status="RUNNING"
        )

        # ------------------------------
        # Abrir sesión 3270
        # ------------------------------
        session = Socket3270Session(
            host="127.0.0.1",
            port=5000
        )
        session.connect()

        # ------------------------------
        # Ejecutar Flow
        # ------------------------------
        matcher = ScreenMatcher()
        flow = LoginFlow(session, matcher)

        result = flow.run(
            username=username,
            password=password
        )

        # ------------------------------
        # Persistir resultado
        # ------------------------------
        if result["status"] == "SUCCESS":
            update_task(
                db=db,
                task_id=self.request.id,
                status="DONE",
                result=str(result)
            )
        else:
            update_task(
                db=db,
                task_id=self.request.id,
                status="FAILED",
                error=result.get("message")
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
        if session:
            session.close()
        db.close()
