"""
screen_matcher.py

Responsable de identificar el tipo de pantalla 3270
a partir del texto renderizado.

NO ejecuta acciones.
NO modifica estado.
"""

from enum import Enum
from typing import Optional


class ScreenType(str, Enum):
    LOGIN = "LOGIN"
    ERROR = "ERROR"
    MENU = "MENU"
    UNKNOWN = "UNKNOWN"


class ScreenMatcher:
    """
    Identifica el tipo de pantalla actual.
    """

    @staticmethod
    def detect(screen_text: str) -> ScreenType:
        """
        Analiza el texto de la pantalla y retorna el tipo.
        """

        normalized = screen_text.upper()

        # ------------------------------
        # LOGIN
        # ------------------------------
        if "ENTER USER ID" in normalized:
            return ScreenType.LOGIN

        # ------------------------------
        # ERROR
        # ------------------------------
        if "INVALID PASSWORD" in normalized:
            return ScreenType.ERROR

        # ------------------------------
        # MENU
        # ------------------------------
        if "MAIN MENU" in normalized:
            return ScreenType.MENU

        # ------------------------------
        # DESCONOCIDA
        # ------------------------------
        return ScreenType.UNKNOWN
