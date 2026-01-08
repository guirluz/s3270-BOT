"""
login_failed_contract.py

Contrato para pantalla de login fallido.
"""

from app.bot.screen.screen_contract import ScreenContract


class LoginFailedScreenContract(ScreenContract):
    name = "LOGIN_FAILED"

    ERROR_KEYWORDS = [
        "INVALID",
        "INCORRECT",
        "NOT AUTHORIZED",
        "ERROR",
    ]

    def matches(self, screen_text: str) -> bool:
        if not screen_text:
            return False

        text = screen_text.upper()

        return any(keyword in text for keyword in self.ERROR_KEYWORDS)
