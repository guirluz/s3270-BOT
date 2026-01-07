"""
celery_app.py

Configuración central de Celery para el proyecto s3270-bot.
Fuerza el uso de Redis como broker y backend.
"""

import os
from celery import Celery
from dotenv import load_dotenv

# ------------------------------------------------------
# Cargar variables de entorno
# ------------------------------------------------------
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# ------------------------------------------------------
# Crear instancia de Celery (FORZANDO Redis)
# ------------------------------------------------------
celery_app = Celery(
    "s3270_bot",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.bot_tasks"],  # 👈 fuerza carga explícita
)

# ------------------------------------------------------
# CONFIGURACIÓN CRÍTICA (ANTI-AMQP)
# ------------------------------------------------------
celery_app.conf.update(
    broker_url=REDIS_URL,
    result_backend=REDIS_URL,

    # 🔥 ESTO ES LO QUE SOLUCIONA TODO
    broker_transport="redis",
    result_backend_transport="redis",

    # Seguridad / serialización
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    timezone="UTC",
    enable_utc=True,

    task_track_started=True,
    task_time_limit=600,
)

# ------------------------------------------------------
# Autodiscover desactivado (evita ambigüedad)
# ------------------------------------------------------
# celery_app.autodiscover_tasks(["app.tasks"])

