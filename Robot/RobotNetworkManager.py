import socket
import time
from threading import Thread


class NetworkDataClient:
    def __init__(self, rdm, lgm):
        self.config = rdm.config['network']
        self.rdm = rdm
        self.lgm = lgm
        self.local_address = rdm.local_address
        self.last_cmd = [127, 127, 127, 127]
        self.rx_thread = Thread(target=self.rx_void, daemon=True, args=())
        self.rx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        self.lgm.dlg('ROBOT', 3, '[RX] Открываю сокет: '+str((self.local_address, int(self.config['data_port']))))
        try:
            self.rx_socket.bind((self.local_address, int(self.config['data_port'])))
            self.lgm.dlg('ROBOT', 3, '[RX] Сокет открыт: '+str((self.local_address, int(self.config['data_port']))))
        except Exception as e:
            self.lgm.dlg('ROBOT', 1, '[RX] Ошибка привязки сокета: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.rx_thread.start()

    def receive(self):
        return self.last_cmd

    def rx_void(self):
        self.rx_socket.listen(1)
        while True:
            self.lgm.dlg('ROBOT', 0, '[RX] Ожидаю подключений...')
            connection, client_address = self.rx_socket.accept()
            try:
                self.lgm.dlg('HOST', 0, '[RX] Подключён клиент: ' + str(client_address) + ".")
                self.rdm.set_remote_address(str(client_address[0]))
                self.rdm.lazy_process_start()
                while True:
                    data = connection.recv(4)
                    self.last_cmd = list(data)
                    time.sleep(0.008)
            except Exception as e:
                self.lgm.dlg('HOST', 1, '[RX] Ошибка подключения или передачи: ' + str(e))
                self.rdm.drop_remote_address()
            time.sleep(1)


class NetworkCommandClient:
    def __init__(self, rdm, lgm):
        self.config = rdm.config['network']
        self.rdm = rdm
        self.lgm = lgm
        self.telemetry = []
        self.local_address = rdm.local_address
        self.mx_thread = Thread(target=self.mx_void, daemon=True, args=())
        self.mx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        self.lgm.dlg('ROBOT', 3, '[MX] Открываю сокет: '+str((self.local_address, int(self.config['command_port']))))
        try:
            self.mx_socket.bind((self.local_address, int(self.config['command_port'])))
            self.lgm.dlg('ROBOT', 3, '[MX] Сокет открыт: '+str((self.local_address, int(self.config['command_port']))))
        except Exception as e:
            self.lgm.dlg('ROBOT', 1, '[MX] Ошибка привязки сокета: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.mx_thread.start()

    def send_telemetry(self, data):
        self.telemetry = data

    def mx_void(self):
        self.mx_socket.listen(1)
        while True:
            self.lgm.dlg('ROBOT', 0, '[MX] Ожидаю подключений...')
            connection, client_address = self.mx_socket.accept()
            try:
                self.lgm.dlg('HOST', 0, '[MX] Подключён клиент: ' + str(client_address) + ".")
                while True:
                    data = connection.recv(1)
                    command = list(data)
                    if command[0] == 2:
                        time.sleep(2)
                        connection.sendall(bytes(self.rdm.get_init_data()))
                    if command[0] == 1:
                        connection.sendall(bytes(self.telemetry))
                    time.sleep(0.008)
            except Exception as e:
                self.lgm.dlg('HOST', 1, '[MX] Ошибка подключения или передачи: ' + str(e))
                self.rdm.drop_remote_address()
            time.sleep(1)
