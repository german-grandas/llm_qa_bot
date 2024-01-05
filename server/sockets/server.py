import socket
import threading
import logging

from controllers.chatbot_controller import ChatBotController


class ChatServer:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sessions = {}
        self.host = host
        self.port = port
        self.threads = {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        logging.info(f"Server listening on {self.host}:{self.port}")
        chatbot_controller = ChatBotController()
        chatbot_controller.initialize()

        while True:
            client_socket, client_address = self.server_socket.accept()
            logging.info(f"Accepted connection from {client_address}")

            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket, client_address)
            )
            self.threads[client_address] = client_thread
            client_thread.start()

    def handle_client(self, client_socket, client_address):
        username = client_socket.recv(1024).decode()
        logging.info(f"User '{username}' connected")

        self.sessions[username] = client_socket

        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.broadcast(username, message)

            except ConnectionError as e:
                logging.info(e)
                break

    def broadcast(self, sender, message):
        chatbot_controller = ChatBotController()
        logging.info("Into broadcast")
        logging.info(f"{sender}, {message}")
        for username, user_socket in self.sessions.items():
            if username == sender:
                try:
                    bot_response = chatbot_controller.query(message)
                    user_socket.sendall(f"bot_response: {bot_response}".encode())
                    logging.info("Message sent")
                except ConnectionError:
                    del self.sessions[username]
                    logging.info(f"User '{username}' disconnected unexpectedly")
