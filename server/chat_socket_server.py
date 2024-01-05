import os
import logging

from sockets.server import ChatServer

HOST = os.environ.get("CHAT_HOST") or "localhost"
PORT = int(os.environ.get("CHAT_PORT") or 12345)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def main():
    server_socket = ChatServer(HOST, PORT)
    server_socket.start()


if __name__ == "__main__":
    main()
