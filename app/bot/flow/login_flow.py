"""
login_flow.py

Flow controller para el proceso de login 3270.
"""

from app.bot.actions.action_factory import ActionFactory
from app.bot.flow.waiter import ScreenWaiter


class LoginFlow:
    """
    Controla el flujo completo del login 3270.
    """

    def __init__(self, session, screen_matcher):
        self.session = session
        self.screen_matcher = screen_matcher
        self.waiter = ScreenWaiter(session, screen_matcher)

    def run(self, username: str, password: str) -> dict:
        max_steps = 10
        step = 0

        while step < max_steps:
            step += 1

            screen_text = self.session.read_screen()
            screen_type = self.screen_matcher.detect(screen_text)

            # Ejecutar acción asociada a la pantalla
            action = ActionFactory.get_action(
                screen_type,
                self.session
            )

            if action:
                action.execute(
                    username=username,
                    password=password
                )

            # Esperar transición lógica
            try:
                next_screen = self.waiter.wait_for_screen(
                    expected_screens=[
                        "LOGIN",
                        "LOGIN_FAILED",
                        "MAIN_MENU",
                    ],
                    timeout=8,
                )
            except TimeoutError:
                return {
                    "status": "FAILED",
                    "message": "Screen transition timeout"
                }

            if next_screen == "LOGIN_FAILED":
                return {
                    "status": "FAILED",
                    "message": "Invalid credentials"
                }

            if next_screen == "MAIN_MENU":
                return {
                    "status": "SUCCESS",
                    "message": "Login successful"
                }

        return {
            "status": "FAILED",
            "message": "Login flow max steps exceeded"
        }

