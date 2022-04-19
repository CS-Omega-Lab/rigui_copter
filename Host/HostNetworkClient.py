import socket
import time
from threading import Thread


class NetworkClient:
    def __init__(self, srs, config):
        self.config = config
        self.srs = srs
        self.data = []
        self.tx_thread = Thread(target=self.tx_void, daemon=True, args=())
        self.tx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tx_socket.bind((config['ip'], int(config['port'])))

    def start(self):
        self.tx_thread.start()
        self.srs.lg('HOST', 0, 'Запуск tx-сокета ('+self.config['port']+'): успешно.')
        return self

    def send_info(self, data):
        self.data = data

    def tx_void(self):
        self.tx_socket.listen(1)
        while True:
            self.srs.lg('HOST', 0, 'Ожидаю подключений...')
            connection, client_address = self.tx_socket.accept()
            try:
                self.srs.lg('HOST', 0, 'Подключён клиент: ' + str(client_address) + ".")
                while True:
                    connection.sendall(bytes(self.data))
                    time.sleep(0.01)
            except Exception as e:
                # self.srs.lg('HOST', 1, 'Ошибка подключения или передачи: ' + str(e))
                self.srs.lg('HOST', 1, 'Ошибка подключения или передачи.')
            time.sleep(1)
