"""
celery_app.py

Configuración central de Celery para el proyecto s3270-bot.

Responsabilidades:
- Inicializar la instancia de Celery
- Conectar con Redis como broker y backend
- Definir serialización segura
- Permitir auto-descubrimiento de tareas

Este archivo NO define tareas.
Solo define la infraestructura.
"""

import os
from celery import Celery
from dotenv import load_dotenv

# ------------------------------------------------------
# Cargar variables de entorno (.env)
# ------------------------------------------------------
load_dotenv()

# ------------------------------------------------------
# Variables de conexión a Redis
# ------------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

# Broker y backend de Celery
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# ------------------------------------------------------
# Crear instancia de Celery
# ------------------------------------------------------
celery_app = Celery(
    "s3270_bot",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# ------------------------------------------------------
# Configuración global de Celery
# ------------------------------------------------------
celery_app.conf.update(
    # Serialización segura (JSON)
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    # Zona horaria
    timezone="UTC",
    enable_utc=True,

    # Manejo de tareas
    task_track_started=True,
    task_time_limit=60 * 10,      # 10 minutos máximo por tarea
    task_soft_time_limit=60 * 9,  # aviso previo
)

# ------------------------------------------------------
# Auto-descubrimiento de tareas
# ------------------------------------------------------
# Celery buscará tareas en app/tasks/*.py
celery_app.autodiscover_tasks([
    "app.tasks"
])
