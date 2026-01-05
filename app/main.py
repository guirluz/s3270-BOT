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

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.bot.session import Socket3270Session
from app.bot.actions import LoginAction
from app.utils.responses import build_response
from app.config.database import get_db
from app.api.uploads import router as uploads_router


# ======================================================
# Inicialización de FastAPI (ESTO VA PRIMERO)
# ======================================================

app = FastAPI(
    title="S3270 Bot API",
    description="API para ejecutar flujos 3270 simulados",
    version="1.0.0",
)


# ======================================================
# Registro de routers (DESPUÉS de crear app)
# ======================================================

app.include_router(uploads_router)


# ======================================================
# Modelos de entrada
# ======================================================

class LoginRequest(BaseModel):
    """
    Modelo de entrada para el endpoint de login.
    """
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
