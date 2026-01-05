# → Analiza texto que devuelve el mainframe
# → Busca pantallas, errores, estados

# app/bot/parser.py


class ScreenParser:
    """
    Analiza el contenido textual de una pantalla 3270.
    """

    def __init__(self, screen_text: str):
        self.screen_text = screen_text.lower()

    def is_login_success(self) -> bool:
        """
        Determina si el login fue exitoso.
        """
        success_keywords = [
            "menu principal",
            "bienvenido",
            "welcome",
            "main menu"
        ]

        return any(keyword in self.screen_text for keyword in success_keywords)

    def is_login_error(self) -> bool:
        """
        Determina si hubo error de login.
        """
        error_keywords = [
            "invalid",
            "incorrect",
            "error",
            "password",
            "usuario no válido",
            "credenciales"
        ]

        return any(keyword in self.screen_text for keyword in error_keywords)

    def is_empty(self) -> bool:
        """
        Pantalla vacía o sin contenido relevante.
        """
        return not self.screen_text.strip()
