"""
screen_contract.py

Contrato base para definir y validar pantallas 3270.
"""

from abc import ABC, abstractmethod


class ScreenContract(ABC):
    """
    Contrato que define cómo reconocer una pantalla 3270.
    """

    name: str

    @abstractmethod
    def matches(self, screen_text: str) -> bool:
        """
        Determina si el texto corresponde a esta pantalla.
        """
        pass
