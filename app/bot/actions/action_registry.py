"""
action_registry.py

Registro central que mapea tipos de pantalla 3270
a sus acciones correspondientes.
"""

from app.bot.actions.login_action import LoginScreenAction


class ActionRegistry:
    """
    Registro estático de pantallas → Actions.
    """

    _registry = {
        "LOGIN": LoginScreenAction,
        # Futuro:
        # "PASSWORD_EXPIRED": PasswordExpiredAction,
        # "SESSION_EXPIRED": SessionExpiredAction,
    }

    @classmethod
    def get_action_class(cls, screen_type: str):
        """
        Devuelve la clase Action asociada a una pantalla.
        """
        return cls._registry.get(screen_type)
