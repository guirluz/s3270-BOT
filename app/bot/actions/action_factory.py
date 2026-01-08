"""
action_factory.py

Factory responsable de instanciar acciones
según el tipo de pantalla detectado.
"""

from app.bot.actions.action_registry import ActionRegistry


class ActionFactory:
    """
    Crea instancias de acciones según la pantalla.
    """

    @staticmethod
    def get_action(screen_type: str, session):
        action_class = ActionRegistry.get_action_class(screen_type)

        if not action_class:
            return None

        return action_class(session)
