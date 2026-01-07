"""
login_failed_action.py

Acción para pantalla de login fallido.
"""

from app.bot.actions.base import ScreenAction


class LoginFailedAction(ScreenAction):
    """
    Maneja pantalla de credenciales inválidas.
    """

    def execute(self, **kwargs):
        # No hay nada que hacer: el Flow terminará
        pass
