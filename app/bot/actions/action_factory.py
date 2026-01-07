"""
action_factory.py

Devuelve la acción correcta según tipo de pantalla.
"""

from app.bot.actions.login_action import LoginScreenAction
from app.bot.actions.login_failed_action import LoginFailedAction
from app.bot.actions.main_menu_action import MainMenuAction


class ActionFactory:

    @staticmethod
    def get_action(screen_type: str, session):
        if screen_type == "LOGIN":
            return LoginScreenAction(session)

        if screen_type == "LOGIN_FAILED":
            return LoginFailedAction(session)

        if screen_type == "MAIN_MENU":
            return MainMenuAction(session)

        return None
