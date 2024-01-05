import socket
import threading
import logging


class ChatClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.username = "main_user"
        self.messages = []
        self.connected = False
        self.received_message = None

        # Connect to the server in a separate thread
        connect_thread = threading.Thread(target=self.connect_to_server)
        connect_thread.start()

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_address, self.server_port))
            self.connected = True
            logging.info("Connected to server")

            # Send the username to the server
            self.client_socket.sendall(self.username.encode())

            # Start a thread to receive messages from the server
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()

        except Exception as e:
            raise e

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    message = message.replace("bot_response:", "")
                    self.received_message = message
                    self.receive_thread.join()

            except Exception as e:
                logging.info(f"Error receiving message: {e}")
                break

    def send_message(self, message_input):
        if self.connected and message_input:
            try:
                message = f"{message_input}"
                self.client_socket.sendall(message.encode())
                self.messages.append(message)
                self.message_input = ""
                self.received_message = None
            except Exception as e:
                logging.info(f"Error sending message: {e}")
