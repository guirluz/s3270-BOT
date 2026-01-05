"""
settings.py

Centraliza la configuración de la aplicación.
Lee variables de entorno para evitar valores hardcodeados.
"""

import os


class Settings:
    """
    Contenedor de configuración global de la aplicación.
    """

    DB_USER: str = os.getenv("DB_USER", "s3270_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "s3270_password")
    DB_NAME: str = os.getenv("DB_NAME", "s3270_db")
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))

    @property
    def database_url(self) -> str:
        """
        Construye la URL de conexión a PostgreSQL.
        """
        return (
            f"postgresql://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


# Instancia global de configuración
settings = Settings()
