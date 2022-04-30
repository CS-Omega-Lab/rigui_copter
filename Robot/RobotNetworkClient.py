import socket
import time
from threading import Thread


class NetworkClient:
    def __init__(self, rdm):
        self.config = rdm.config['general']
        self.rdm = rdm
        self.last_cmd = None
        self.rx_thread = Thread(target=self.rx_void, daemon=True, args=())
        self.rx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        self.rdm.lg('ROBOT', 0, 'Подключаюсь к сокету: ' + self.config['ip'] + ":" + self.config['port'])
        try:
            self.rx_socket.connect((self.config['ip'], int(self.config['port'])))
            self.rdm.lg('ROBOT', 0, 'Подключён к сокету: '+self.config['ip']+":"+self.config['port'])
        except Exception as e:
            self.rdm.lg('ROBOT', 1, 'Ошибка подключения к сокету: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.rx_thread.start()

    def receive(self):
        return self.last_cmd

    def rx_void(self):
        while True:
            data = self.rx_socket.recv(8)
            self.last_cmd = list(data)
            if data == bytes((255, 255, 255, 255, 255, 255, 255, 255)):
                self.rx_socket.sendall(bytes((255, 255, 255, 255, 255, 255, 255, 255)))
            time.sleep(0.008)
