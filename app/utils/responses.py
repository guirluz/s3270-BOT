"""
responses.py

Módulo utilitario para la construcción uniforme de respuestas HTTP
en la API FastAPI del bot 3270.

Objetivos:
- Centralizar la estructura de las respuestas JSON
- Garantizar consistencia en todos los endpoints
- Evitar duplicación de código
- Facilitar mantenimiento y escalabilidad

Todas las respuestas de la API DEBEN construirse usando este módulo.
"""

from typing import Any, Optional, Dict
from fastapi.responses import JSONResponse


def _status_from_http_code(http_code: int) -> str:
    """
    Determina el estado lógico de la respuesta en función
    del código HTTP.

    Parámetros:
        http_code (int): Código HTTP de la respuesta.

    Retorna:
        str: Estado lógico ('success', 'processing', 'error').
    """
    if http_code == 200:
        return "success"

    if http_code == 202:
        return "processing"

    if http_code in (400, 404):
        return "error"

    if http_code >= 500:
        return "error"

    return "unknown"


def build_response(
    http_code: int,
    message: str,
    data: Optional[Any] = None
) -> JSONResponse:
    """
    Construye una respuesta HTTP uniforme para la API.

    Esta función debe ser utilizada por TODOS los endpoints.

    Parámetros:
        http_code (int):
            Código HTTP que se desea retornar (200, 400, 404, 202, 500).

        message (str):
            Mensaje descriptivo y entendible para el cliente.

        data (Any, opcional):
            Información adicional a retornar.
            Puede ser un diccionario, lista, string, etc.
            Si no se requiere, se envía como None.

    Retorna:
        JSONResponse:
            Objeto de respuesta listo para FastAPI.
    """

    response_body: Dict[str, Any] = {
        "status": _status_from_http_code(http_code),
        "code": http_code,
        "message": message,
        "data": data
    }

    return JSONResponse(
        status_code=http_code,
        content=response_body
    )
