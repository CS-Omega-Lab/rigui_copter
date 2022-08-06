import socket
import time
from threading import Thread


class NetworkDataClient:
    def __init__(self, rdm):
        self.config = rdm.config['network']
        self.rdm = rdm
        self.last_cmd = []
        self.rx_thread = Thread(target=self.rx_void, daemon=True, args=())
        self.rx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        self.rdm.lg('ROBOT', 0, '[RX] Подключаюсь к сокету: ' + self.config['host'] + ":" + self.config['data_port'])
        try:
            self.rx_socket.connect((self.config['host'], int(self.config['data_port'])))
            self.rdm.lg('ROBOT', 0, '[RX] Подключён к сокету: '+self.config['host']+":"+self.config['data_port'])
        except Exception as e:
            self.rdm.lg('ROBOT', 1, '[RX] Ошибка подключения к сокету: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.rx_thread.start()

    def receive(self):
        return self.last_cmd

    def rx_void(self):
        while True:
            data = self.rx_socket.recv(9)
            self.last_cmd = list(data)
            time.sleep(0.008)


class NetworkCommandClient:
    def __init__(self, rdm):
        self.config = rdm.config['network']
        self.rdm = rdm
        self.telemetry = []
        self.mx_thread = Thread(target=self.mx_void, daemon=True, args=())
        self.mx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        self.rdm.lg('ROBOT', 0, '[MX] Подключаюсь к сокету: ' + self.config['host'] + ":" + self.config['command_port'])
        try:
            self.mx_socket.connect((self.config['host'], int(self.config['command_port'])))
            self.rdm.lg('ROBOT', 0, '[MX] Подключён к сокету: '+self.config['host']+":"+self.config['command_port'])
        except Exception as e:
            self.rdm.lg('ROBOT', 1, '[MX] Ошибка подключения к сокету: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.mx_thread.start()

    def send_telemetry(self, data):
        self.telemetry = data

    def mx_void(self):
        while True:
            data = self.mx_socket.recv(1)
            command = list(data)
            if command[0] == 2:
                time.sleep(2)
                self.mx_socket.sendall(bytes(self.rdm.get_init_data()))
            if command[0] == 1:
                self.mx_socket.sendall(bytes(self.telemetry))
            time.sleep(0.008)
