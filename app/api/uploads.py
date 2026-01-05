"""
uploads.py

Endpoints relacionados con la tabla uploads.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.upload import Upload
from app.utils.responses import build_response

router = APIRouter(prefix="/uploads", tags=["Uploads"])


@router.post("/", status_code=status.HTTP_200_OK)
def create_upload(filename: str, db: Session = Depends(get_db)):
    """
    Crea un registro de upload en la base de datos.

    - filename: nombre del archivo (string)
    """

    try:
        if not filename.strip():
            return error_response(
                message="Filename cannot be empty",
                code=400
            )

        upload = Upload(filename=filename)

        db.add(upload)
        db.commit()
        db.refresh(upload)

        return success_response(
            message="Upload created successfully",
            data={
                "id": upload.id,
                "filename": upload.filename,
                "created_at": upload.created_at
            }
        )

    except Exception as exc:
        db.rollback()

        return error_response(
            message="Failed to create upload",
            data=str(exc),
            code=500
        )
