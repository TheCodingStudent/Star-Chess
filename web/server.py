import time
import socket
from threading import Thread

KB = 16

class Server:
    """Server class"""
    def __init__(self):

        # Properties
        self.host = '25.73.52.143'
        self.port = 55555
        self.clients = list()
        self.threads = list()

        # Server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

    def broadcast(self, message: bytes) -> None:
        """Sends a message to all clients"""
        print('broadcasting ', message)
        if not isinstance(message, bytes): message = message.encode()
        for client in self.clients:
            client.send(message)

    def handle(self, client: socket.socket) -> None:
        """Handles the connection with each client"""
        while self.listening:
            try:
                message = client.recv(1024*KB).decode()
                if message:
                    print(f'server: {message}')
                    self.broadcast(message)
            except Exception as e:
                print(e)
                self.clients.remove(client)
                client.close()
                print(f'clients: {len(self.clients)}')
                if not self.clients:
                    self.listening = False
                    return
        print('handle stopped')

    def close(self) -> None:
        """Closes the connection"""
        self.listening = False
        print('closing server...', len(self.threads))
        self.threads.clear()

    def receive(self) -> None:
        """Checks for new connections"""
        self.listening = True
        try:
            while self.listening:
                client, address = self.server.accept()

                client.send('connected'.encode())
                response = client.recv(1024*KB).decode()
                if not response: 
                    print('cliente no conectado')
                    continue
            
                self.clients.append(client)
                print(f'cliente conectado con exito: {len(self.clients)}')

                thread = Thread(target=self.handle, args=(client,), daemon=True)
                self.threads.append(thread)
                thread.start()
        except KeyboardInterrupt:
            self.listening = False
        


if __name__ == '__main__':
    server = Server()
    server.receive()
    print('server started')