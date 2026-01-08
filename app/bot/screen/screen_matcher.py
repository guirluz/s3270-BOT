"""
screen_matcher.py

Responsable de identificar el tipo de pantalla 3270
basándose en el texto recibido desde la sesión.
"""

class ScreenMatcher:
    """
    Detecta qué pantalla 3270 está activa a partir del texto completo.
    """

    def detect(self, screen_text: str) -> str:
        """
        Devuelve un identificador lógico de pantalla.

        Posibles valores:
        - LOGIN
        - LOGIN_FAILED
        - UNKNOWN
        """

        if not screen_text:
            return "UNKNOWN"

        text = screen_text.upper()

        # --------------------------------
        # LOGIN FALLIDO (prioridad alta)
        # --------------------------------
        if any(keyword in text for keyword in (
            "INVALID",
            "ERROR",
            "NOT AUTHORIZED",
            "INCORRECT",
        )):
            return "LOGIN_FAILED"

        # --------------------------------
        # PANTALLA DE LOGIN
        # --------------------------------
        if any(keyword in text for keyword in (
            "USER",
            "USERNAME",
            "PASSWORD",
            "LOGON",
            "SIGN ON",
        )):
            return "LOGIN"

        # --------------------------------
        # DESCONOCIDA (por ahora)
        # --------------------------------
        return "UNKNOWN"
