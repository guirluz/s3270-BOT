"""
main.py

Punto de entrada de la aplicación FastAPI.

Responsabilidades:
- Exponer endpoints HTTP
- Validar datos de entrada
- Orquestar la ejecución del bot
- Construir respuestas HTTP uniformes

Este archivo NO contiene lógica 3270 ni lógica de negocio.
"""

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.bot.session import Socket3270Session
from app.bot.actions import LoginAction
from app.utils.responses import build_response
from app.config.database import get_db
from app.api.uploads import router as uploads_router
from app.tasks.bot_tasks import login_bot_task
from app.celery_app import celery_app
from app.db.models.task import TaskExecution
from app.db.session import SessionLocal

# IMPORTS CLAVE PARA CREAR TABLAS
from app.db.base import Base
from app.db.session import engine


# ======================================================
# Inicialización de FastAPI (ESTO VA PRIMERO)
# ======================================================

app = FastAPI(
    title="S3270 Bot API",
    description="API para ejecutar flujos 3270 simulados",
    version="1.0.0",
)


# ======================================================
# CREAR TABLAS AUTOMÁTICAMENTE (SOLO DEV)
# ======================================================

Base.metadata.create_all(bind=engine)


# ======================================================
# Registro de routers
# ======================================================

app.include_router(uploads_router)


# ======================================================
# Modelos de entrada
# ======================================================

class LoginRequest(BaseModel):
    user: str
    password: str


class AsyncLoginRequest(BaseModel):
    user: str
    password: str


# ======================================================
# Endpoints
# ======================================================

@app.post("/login")
def login(request: LoginRequest):
    """
    Ejecuta el flujo de login 3270 contra el host simulado.
    """

    session = None

    try:
        if not request.user or not request.user.strip():
            return build_response(400, "User is required", None)

        if not request.password or not request.password.strip():
            return build_response(400, "Password is required", None)

        session = Socket3270Session(host="127.0.0.1", port=5000)
        session.connect()

        login_action = LoginAction(session)
        screen = login_action.execute(
            username=request.user,
            password=request.password
        )

        return build_response(
            http_code=200,
            message="Login successful",
            data={"screen": screen}
        )

    except ConnectionRefusedError:
        return build_response(404, "3270 host not available", None)

    except RuntimeError as exc:
        return build_response(400, str(exc), None)

    except Exception:
        return build_response(500, "Internal server error", None)

    finally:
        if session:
            session.close()


# ======================================================
# Health check DB
# ======================================================

@app.get("/health/db")
def database_health(db: Session = Depends(get_db)):
    """
    Verifica que la base de datos está accesible.
    """
    try:
        db.execute(text("SELECT 1"))
        return build_response(200, "Database connection OK", None)
    except Exception as exc:
        return build_response(500, "Database connection failed", str(exc))


# --------------------
# Valida datos, encola la tarea en redis, devuelve task_id, responde http 202
# --------------------

@app.post("/tasks/login")
def start_login_task(request: AsyncLoginRequest):
    """
    Lanza una tarea asíncrona de login 3270.

    Flujo:
    1. Valida datos de entrada
    2. Encola tarea en Celery (Redis)
    3. Registra la tarea en PostgreSQL
    4. Retorna HTTP 202 con task_id
    """

    db = None

    try:
        # -------------------------------------------------
        # Validaciones de entrada
        # -------------------------------------------------
        if not request.user or not request.user.strip():
            return build_response(400, "User is required", None)

        if not request.password or not request.password.strip():
            return build_response(400, "Password is required", None)

        # -------------------------------------------------
        # Encolar tarea en Celery
        # -------------------------------------------------
        task = login_bot_task.delay(
            username=request.user,
            password=request.password
        )

        # -------------------------------------------------
        # Registrar tarea en PostgreSQL (estado inicial)
        # -------------------------------------------------
        db = next(get_db())

        from app.tasks.task_repository import create_task

        create_task(
            db=db,
            task_id=task.id,
            task_type="LOGIN",
            status="PENDING",
        )

        # -------------------------------------------------
        # Respuesta inmediata (HTTP 202)
        # -------------------------------------------------
        return build_response(
            http_code=202,
            message="Login task accepted",
            data={
                "task_id": task.id,
                "status": "PENDING"
            }
        )

    except Exception as exc:
        return build_response(
            http_code=500,
            message="Failed to start login task",
            data=str(exc)
        )

    finally:
        if db:
            db.close()


#---------------------------------------

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str, db: Session = Depends(get_db)):
    """
    Consulta el estado actual de una tarea asíncrona.
    """

    task = db.query(TaskExecution).filter(
        TaskExecution.task_id == task_id
    ).first()

    if not task:
        return build_response(
            http_code=404,
            message="Task not found",
            data=None
        )

    # ------------------------------
    # Tarea aún en progreso
    # ------------------------------
    if task.status in ("PENDING", "RUNNING"):
        return build_response(
            http_code=202,
            message="Task still in progress",
            data={
                "task_id": task.task_id,
                "status": task.status
            }
        )

    # ------------------------------
    # Tarea finalizada correctamente
    # ------------------------------
    if task.status == "DONE":
        return build_response(
            http_code=200,
            message="Task completed successfully",
            data={
                "task_id": task.task_id,
                "status": task.status,
                "result": task.result
            }
        )

    # ------------------------------
    # Tarea fallida
    # ------------------------------
    if task.status == "FAILED":
        return build_response(
            http_code=200,
            message="Task completed with business error",
            data={
                "task_id": task.task_id,
                "status": task.status,
                "error": task.error
            }
        )


    # ------------------------------
    # Estado desconocido (no debería pasar)
    # ------------------------------
    return build_response(
        http_code=500,
        message="Unknown task state",
        data={
            "task_id": task.task_id,
            "status": task.status
        }
    )

