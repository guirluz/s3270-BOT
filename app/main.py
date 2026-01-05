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

from fastapi import FastAPI
from pydantic import BaseModel

from app.bot.session import Socket3270Session
from app.bot.actions import LoginAction
from app.utils.responses import build_response


# ======================================================
# Inicialización de FastAPI
# ======================================================

app = FastAPI(
    title="S3270 Bot API",
    description="API para ejecutar flujos 3270 simulados",
    version="1.0.0",
)


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

    Flujo:
    1. Validar datos de entrada
    2. Crear sesión 3270
    3. Ejecutar acción de login
    4. Retornar resultado uniforme
    """

    session = None

    try:
        # ------------------------------
        # Validaciones de entrada
        # ------------------------------
        if not request.user or not request.user.strip():
            return build_response(
                http_code=400,
                message="User is required",
                data=None
            )

        if not request.password or not request.password.strip():
            return build_response(
                http_code=400,
                message="Password is required",
                data=None
            )

        # ------------------------------
        # Crear sesión 3270
        # ------------------------------
        session = Socket3270Session(
            host="127.0.0.1",
            port=5000
        )

        session.connect()

        # ------------------------------
        # Ejecutar acción de login
        # ------------------------------
        login_action = LoginAction(session)
        screen = login_action.execute(
            username=request.user,
            password=request.password
        )

        # ------------------------------
        # Respuesta exitosa
        # ------------------------------
        return build_response(
            http_code=200,
            message="Login successful",
            data={
                "screen": screen
            }
        )

    except ConnectionRefusedError:
        # Host no disponible
        return build_response(
            http_code=404,
            message="3270 host not available",
            data=None
        )

    except RuntimeError as exc:
        # Errores de negocio (login fallido, pantallas inesperadas, etc.)
        return build_response(
            http_code=400,
            message=str(exc),
            data=None
        )

    except Exception:
        # Error inesperado
        return build_response(
            http_code=500,
            message="Internal server error",
            data=None
        )

    finally:
        # ------------------------------
        # Cierre seguro de la sesión
        # ------------------------------
        if session:
            session.close()

