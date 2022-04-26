import socket
import time
from threading import Thread


class NetworkClient:
    def __init__(self):
        self.last_cmd = None
        self.flag = False
        self.rx_thread = Thread(target=self.rx_void, daemon=True, args=())
        self.rx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rx_socket.connect(('192.168.31.32', 5051))

    def start(self):
        self.rx_thread.start()

    def receive(self):
        return self.last_cmd

    def rx_void(self):
        while True:
            data = self.rx_socket.recv(7)
            self.last_cmd = list(data)
            time.sleep(0.009)
