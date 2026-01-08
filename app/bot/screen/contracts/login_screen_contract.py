"""
login_screen_contract.py

Contrato para la pantalla de login 3270.
"""

from app.bot.screen.screen_contract import ScreenContract


class LoginScreenContract(ScreenContract):
    name = "LOGIN"

    REQUIRED_KEYWORDS = [
        "USER",
        "PASSWORD",
        "SIGN ON",
        "LOGON",
    ]

    def matches(self, screen_text: str) -> bool:
        if not screen_text:
            return False

        text = screen_text.upper()

        return all(keyword in text for keyword in self.REQUIRED_KEYWORDS)
