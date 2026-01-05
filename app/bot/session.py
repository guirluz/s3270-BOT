"""
session.py

Controla la comunicación técnica con un host 3270 simulado.
Esta clase será la base para integrar s3270 real en el futuro.
"""

import socket


class Socket3270Session:
    """
    Implementa una sesión 3270 usando un socket TCP.

    Esta clase abstrae la comunicación con el host:
    - conexión
    - envío de comandos
    - recepción de respuestas
    """

    def __init__(self, host: str, port: int):
        """
        Inicializa la sesión con la dirección del host.

        :param host: dirección IP o hostname del host 3270
        :param port: puerto TCP del host
        """
        self.host = host
        self.port = port
        self.socket: socket.socket | None = None

    def connect(self) -> None:
        """
        Abre la conexión TCP con el host 3270.

        Lanza una excepción si no puede conectar.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_command(self, command: str) -> str:
        """
        Envía un comando al host y espera la respuesta.

        :param command: comando a enviar (ej: CONNECT, LOGIN user pass)
        :return: texto de la pantalla devuelta por el host
        """
        if not self.socket:
            raise RuntimeError("Session is not connected")

        # Enviar comando con salto de línea
        self.socket.sendall((command + "\n").encode("utf-8"))

        # Recibir respuesta del host
        data = self.socket.recv(4096)

        if not data:
            raise RuntimeError("Connection closed by host")

        return data.decode("utf-8").strip()

    def close(self) -> None:
        """
        Cierra la conexión con el host.
        """
        if self.socket:
            self.socket.close()
            self.socket = None

