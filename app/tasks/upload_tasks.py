"""
upload_tasks.py

Tareas Celery para procesar archivos subidos.
"""

import os
import time
import pandas as pd

from celery import shared_task
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models.task import TaskExecution
from app.db.models.upload import Upload


@shared_task(bind=True)
def process_upload_task(self, upload_id: int) -> dict:
    """
    Procesa un archivo subido de forma asíncrona.

    Estados:
    - STARTED
    - SUCCESS
    - FAILURE
    """

    db: Session = SessionLocal()

    try:
        # ---------------------------------
        # Marcar tarea como STARTED
        # ---------------------------------
        self.update_state(
            state="STARTED",
            meta={"step": "loading upload record"}
        )

        upload = db.query(Upload).filter(Upload.id == upload_id).first()

        if not upload:
            raise RuntimeError("Upload record not found")

        file_path = upload.file_path

        if not os.path.exists(file_path):
            raise RuntimeError("Uploaded file not found on disk")

        # ---------------------------------
        # Simular lectura de archivo
        # (aquí luego irá lógica real)
        # ---------------------------------
        self.update_state(
            state="STARTED",
            meta={"step": "reading file"}
        )

        time.sleep(2)

        # Ejemplo: leer CSV o Excel
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        rows = len(df)

        # ---------------------------------
        # Simular procesamiento
        # ---------------------------------
        self.update_state(
            state="STARTED",
            meta={"step": "processing rows"}
        )

        time.sleep(2)

        # ---------------------------------
        # Resultado final
        # ---------------------------------
        return {
            "status": "SUCCESS",
            "rows_processed": rows
        }

    except Exception as exc:
        raise exc

    finally:
        db.close()
