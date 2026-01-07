"""
screen_matcher.py

Responsable de identificar el tipo de pantalla 3270
basándose en el texto recibido.
"""

class ScreenMatcher:
    """
    Detecta qué pantalla 3270 está activa.
    """

    def detect(self, screen_text: str) -> str:
        """
        Devuelve un identificador lógico de pantalla.
        """

        if not screen_text:
            return "UNKNOWN"

        text = screen_text.upper()

        # --------------------------------
        # LOGIN FALLIDO (alta prioridad)
        # --------------------------------
        if any(keyword in text for keyword in [
            "INVALID",
            "ERROR",
            "NOT AUTHORIZED",
            "INCORRECT"
        ]):
            return "LOGIN_FAILED"

        # --------------------------------
        # LOGIN
        # --------------------------------
        if any(keyword in text for keyword in [
            "USER",
            "USERNAME",
            "PASSWORD",
            "LOGON",
            "SIGN ON"
        ]):
            return "LOGIN"

        # --------------------------------
        # MENÚ PRINCIPAL
        # --------------------------------
        if any(keyword in text for keyword in [
            "MAIN MENU",
            "OPTIONS",
            "COMMAND",
            "SELECTION"
        ]):
            return "MAIN_MENU"

        # --------------------------------
        # DESCONOCIDO
        # --------------------------------
        return "UNKNOWN"
