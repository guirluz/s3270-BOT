"""
login_flow.py

Flow controller para el proceso de login 3270.
"""

import time

from app.bot.actions.action_factory import ActionFactory


class LoginFlow:
    """
    Controla el flujo completo del login 3270.
    """

    def __init__(self, session, screen_matcher):
        self.session = session
        self.screen_matcher = screen_matcher

    def run(self, username: str, password: str) -> dict:
        max_steps = 10
        step = 0

        while step < max_steps:
            step += 1

            screen_text = self.session.read_screen()
            screen_type = self.screen_matcher.detect(screen_text)

            action = ActionFactory.get_action(
                screen_type,
                self.session
            )

            if action:
                action.execute(
                    username=username,
                    password=password
                )

            if screen_type == "LOGIN_FAILED":
                return {
                    "status": "FAILED",
                    "message": "Invalid credentials"
                }

            if screen_type == "MAIN_MENU":
                return {
                    "status": "SUCCESS",
                    "message": "Login successful"
                }

            time.sleep(0.5)

        return {
            "status": "FAILED",
            "message": "Login flow timeout"
        }

