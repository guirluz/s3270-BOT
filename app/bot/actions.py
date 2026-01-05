"""
actions.py

Define las acciones de alto nivel que ejecuta el bot 3270.
Aquí vive la lógica del negocio, no la comunicación.
"""

from app.bot.session import Socket3270Session


class LoginAction:
    """
    Acción de login contra un host 3270.

    Esta clase encapsula el flujo completo de autenticación.
    """

    def __init__(self, session: Socket3270Session):
        """
        Inicializa la acción con una sesión activa.

        :param session: instancia de Socket3270Session
        """
        self.session = session

    def execute(self, username: str, password: str) -> str:
        """
        Ejecuta el flujo de login.

        :param username: usuario a autenticar
        :param password: contraseña
        :return: pantalla final tras el login
        """

        # Paso 1: iniciar conexión lógica
        response = self.session.send_command("CONNECT")

        if "LOGIN" not in response:
            raise RuntimeError("Unexpected screen during CONNECT")

        # Paso 2: enviar credenciales
        response = self.session.send_command(
            f"LOGIN {username} {password}"
        )

        if "MENU" not in response:
            raise RuntimeError("Login failed or unexpected response")

        return response
