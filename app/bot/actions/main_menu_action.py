"""
main_menu_action.py

Acción para pantalla principal tras login exitoso.
"""

from app.bot.actions.base import ScreenAction


class MainMenuAction(ScreenAction):
    """
    Acción al llegar al menú principal.
    """

    def execute(self, **kwargs):
        # Por ahora no hacemos nada
        pass
