"""
waiter.py

Utilidades para esperar cambios de pantalla 3270
de forma segura y determinística.
"""

import time


class ScreenWaiter:
    """
    Espera activa hasta que aparezca una pantalla esperada.
    """

    def __init__(self, session, screen_matcher):
        self.session = session
        self.screen_matcher = screen_matcher

    def wait_for_screen(
        self,
        expected_screens: list[str],
        timeout: float = 10.0,
        poll_interval: float = 0.3,
    ) -> str:
        """
        Espera hasta que aparezca una de las pantallas esperadas.

        Retorna el screen_type detectado.
        Lanza TimeoutError si no aparece ninguna.
        """

        start_time = time.time()

        while time.time() - start_time < timeout:
            screen_text = self.session.read_screen()
            screen_type = self.screen_matcher.detect(screen_text)

            if screen_type in expected_screens:
                return screen_type

            time.sleep(poll_interval)

        raise TimeoutError(
            f"Timeout waiting for screens {expected_screens}"
        )
