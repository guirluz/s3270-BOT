"""
login_action.py

Acción para la pantalla de login 3270.
"""

from app.bot.actions.base import ScreenAction


class LoginScreenAction(ScreenAction):
    """
    Ingresa usuario y contraseña en pantalla LOGIN.
    """

    def execute(self, username: str, password: str):
        self.session.send_text(username, row=5, col=20)
        self.session.send_text(password, row=6, col=20)
        self.session.send_enter()

