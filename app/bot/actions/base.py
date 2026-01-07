"""
base.py

Clase base para todas las Actions 3270.
"""

from abc import ABC, abstractmethod


class ScreenAction(ABC):
    """
    Contrato base para acciones sobre una pantalla 3270.
    """

    def __init__(self, session):
        self.session = session

    @abstractmethod
    def execute(self, **kwargs):
        """
        Ejecuta la acción sobre la pantalla actual.
        """
        pass
