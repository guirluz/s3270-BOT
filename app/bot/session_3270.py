"""
session_3270.py

Capa de infraestructura para comunicación con un emulador 3270.
NO contiene lógica de negocio.
"""

import time
from typing import Optional


class Session3270:
    """
    Sesión base 3270.

    Esta clase representa una conexión activa a un host/emulador 3270.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connected = False
        self._screen_buffer: Optional[str] = None

    # -------------------------------------------------
    # Conexión
    # -------------------------------------------------
    def connect(self) -> None:
        """
        Conecta con el host 3270.
        """
        # En esta fase es una simulación
        self.connected = True
        self._screen_buffer = (
            "ENTER USER ID ===>\n"
            "ENTER PASSWORD ==>\n"
        )

    def disconnect(self) -> None:
        """
        Cierra la conexión.
        """
        self.connected = False
        self._screen_buffer = None

    # -------------------------------------------------
    # Entrada
    # -------------------------------------------------
    def send_text(self, text: str) -> None:
        """
        Envía texto al buffer de entrada del host.
        """
        if not self.connected:
            raise RuntimeError("Session not connected")

        # Simulación: no cambia pantalla aún
        pass

    def send_enter(self) -> None:
        """
        Simula la tecla ENTER.
        """
        if not self.connected:
            raise RuntimeError("Session not connected")

        # Simulación de cambio de pantalla
        self._screen_buffer = "INVALID PASSWORD\n"

    # -------------------------------------------------
    # Salida
    # -------------------------------------------------
    def read_screen(self) -> str:
        """
        Retorna el contenido actual de la pantalla.
        """
        if not self.connected:
            raise RuntimeError("Session not connected")

        return self._screen_buffer or ""

    # -------------------------------------------------
    # Espera
    # -------------------------------------------------
    def wait_for_screen_change(
        self,
        previous_screen: str,
        timeout: int = 5,
        poll_interval: float = 0.2,
    ) -> str:
        """
        Espera hasta que la pantalla cambie o se agote el timeout.
        """
        start = time.time()

        while time.time() - start < timeout:
            current = self.read_screen()
            if current != previous_screen:
                return current
            time.sleep(poll_interval)

        raise TimeoutError("Screen did not change within timeout")
