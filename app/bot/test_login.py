"""
test_login.py

Script de prueba para validar el flujo completo del bot 3270
usando el host simulado.
"""

from app.bot.session import Socket3270Session
from app.bot.actions import LoginAction


def main():
    """
    Ejecuta una prueba completa de login contra el host simulado.
    """

    # Configuración del host simulado
    host = "127.0.0.1"
    port = 5000

    # Crear sesión 3270
    session = Socket3270Session(host, port)

    try:
        # Conectar al host
        print("Connecting to host...")
        session.connect()

        # Ejecutar acción de login
        login_action = LoginAction(session)
        result = login_action.execute(
            username="admin",
            password="admin"
        )

        # Mostrar resultado
        print("Login result:")
        print(result)

    finally:
        # Cerrar sesión
        session.close()
        print("Session closed")


if __name__ == "__main__":
    main()
