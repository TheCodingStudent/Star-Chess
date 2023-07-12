import time
import socket
import threading

KB = 16


class Client:
    """Client class"""
    def __init__(self, ip: str='25.73.52.143', port: int=55555):
        self.port = port
        self.ip = ip
        self.connected = False

    def connect(self, ip: str='', port: int=0) -> None:
        """Connects to the given IP and port"""

        # UPDATE IP OR PORT
        if ip: self.ip = ip
        if port: self.port = port

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
        self.send_message('received')
        while self.connected:
            try:
                message = self.client.recv(1024*KB).decode()
                print(f'sending: {message=}')
                self.on_receive(message)
            except:
                self.client.close()
                break
    
    def close(self) -> None:
        """Closes the client"""
        self.connected = False
        self.client.close()

    def send_message(self, message: str, wait_time: float=0) -> None:
        """Sends a message back to server"""
        if not isinstance(message, bytes): message = message.encode()
        print(f'sending from client: {message}')
        if wait_time: time.sleep(wait_time)
        self.client.send(message)