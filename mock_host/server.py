"""
Mock 3270 Host

Este módulo implementa un host 3270 simulado usando sockets TCP.
Su objetivo es comportarse como un mainframe IBM real para pruebas
y desarrollo de bots basados en s3270/x3270.

No implementa el protocolo TN3270 real, sino una simulación lógica
del flujo de pantallas y comandos.
"""

import socket

# Dirección y puerto donde el host 3270 simulado escuchará conexiones
HOST = "127.0.0.1"
PORT = 5000


class Mock3270Host:
    """
    Simula un mainframe 3270 mediante una máquina de estados.

    Cada estado representa una pantalla típica de un sistema IBM:
    - INIT        : Host iniciado, esperando conexión
    - LOGIN       : Pantalla de login (usuario/clave)
    - MENU        : Menú principal
    - PROCESSING  : Procesamiento de datos
    - RESULT      : Resultado del proceso
    - END         : Fin de sesión
    """

    def __init__(self):
        # Estado inicial del sistema
        self.state = "INIT"

    def handle_command(self, command: str) -> str:
        """
        Procesa un comando recibido desde el cliente (bot/s3270)
        y devuelve una respuesta que simula una pantalla 3270.

        :param command: Comando recibido como texto plano
        :return: Respuesta del host (pantalla o mensaje)
        """
        # Limpia saltos de línea y espacios
        command = command.strip()

        # Estado inicial: se espera un CONNECT
        if self.state == "INIT":
            if command == "CONNECT":
                self.state = "LOGIN"
                return "SCREEN LOGIN"
            return "ERROR Must CONNECT first"

        # Estado de login
        if self.state == "LOGIN":
            if command.startswith("LOGIN"):
                # Formato esperado: LOGIN usuario password
                _, user, password = command.split(maxsplit=2)

                # Credenciales válidas simuladas
                if user == "admin" and password == "admin":
                    self.state = "MENU"
                    return "SCREEN MENU"

                return "ERROR Invalid credentials"

            return "ERROR Expected LOGIN"

        # Estado de menú principal
        if self.state == "MENU":
            if command == "MENU 1":
                self.state = "PROCESSING"
                return "SCREEN PROCESSING"

            if command == "MENU 9":
                self.state = "END"
                return "BYE"

            return "ERROR Invalid menu option"

        # Estado de procesamiento
        if self.state == "PROCESSING":
            if command.startswith("PROCESS"):
                self.state = "RESULT"
                return "SCREEN RESULT total=3 ok=3 error=0"

            return "ERROR Expected PROCESS"

        # Estado no reconocido
        return "ERROR Invalid state"


def start_server():
    """
    Inicia el servidor TCP que actúa como host 3270 simulado.

    Acepta una única conexión y procesa comandos secuencialmente
    hasta que el cliente envía la orden de salida (BYE).
    """
    # Inicializa la lógica del host
    host_logic = Mock3270Host()

    # Crea el socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()

        print(f"Mock 3270 Host listening on {HOST}:{PORT}")

        # Espera conexión del cliente (bot / s3270)
        conn, addr = server.accept()
        with conn:
            print(f"Connection from {addr}")

            while True:
                # Recibe datos del cliente
                data = conn.recv(1024)
                if not data:
                    break

                # Decodifica comando recibido
                command = data.decode("utf-8")

                # Procesa el comando y obtiene respuesta
                response = host_logic.handle_command(command)

                # Envía respuesta al cliente
                conn.sendall((response + "\n").encode("utf-8"))

                # Si el host indica salida, termina la sesión
                if response == "BYE":
                    break


# Punto de entrada del script
if __name__ == "__main__":
    start_server()

