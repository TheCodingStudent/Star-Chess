import socket
import threading

KB = 16


class Client:
    """Client class"""
    def __init__(self, ip: str='25.73.52.143', port: int=55555):
        self.port = port
        self.ip = ip
        self.connected = False

    def connect(self) -> None:
        """Connects to the given IP and port"""
        self.connected = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip, self.port))
        print(f'connected to {(self.ip, self.port)}')
        thread = threading.Thread(target=self.receive, daemon=True)
        thread.start()

    def on_receive(self, message: str) -> None:
        """Template function when a message is received"""

    def receive(self) -> None:
        """Checks for messages"""
        self.connected = True
        while self.connected:
            try:
                message = self.client.recv(1024*KB).decode()
                self.on_receive(message)
            except:
                self.client.close()
                break
    
    def close(self) -> None:
        """Closes the client"""
        self.connected = False
        self.client.close()

    def send_message(self, message: str) -> None:
        """Sends a message back to server"""
        if not isinstance(message, bytes): message = message.encode()
        print(f'sending from client: {message}')
        self.client.send(message)