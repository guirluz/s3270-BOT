"""
login_action.py

Acción asociada a la pantalla de login 3270.
"""

from app.bot.actions.base import ScreenAction


class LoginScreenAction(ScreenAction):
    """
    Action para enviar usuario y contraseña en la pantalla LOGIN.
    """

    def execute(self, username: str, password: str):
        """
        Ejecuta el login sobre la sesión 3270.
        """

        if not username or not password:
            raise ValueError("Username and password required")

        # Escribir usuario
        self.session.write_at(row=10, col=20, text=username)

        # Escribir contraseña
        self.session.write_at(row=11, col=20, text=password)

        # Enviar Enter
        self.session.send_enter()

