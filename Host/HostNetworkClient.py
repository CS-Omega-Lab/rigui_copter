import socket
import time
from threading import Thread


class NetworkClient:
    def __init__(self, hdm, config):
        self.config = config
        self.hdm = hdm
        self.data = []
        self.tx_thread = Thread(target=self.tx_void, daemon=True, args=())
        self.tx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        self.ping = False
        try:
            self.tx_socket.bind((config['ip'], int(config['port'])))
        except Exception as e:
            self.hdm.lg('HOST', 1, 'Ошибка привязки сокета: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.tx_thread.start()
            self.hdm.lg('HOST', 0, 'Запуск tx-сокета (' + self.config['port'] + '): успешно.')
        return self

    def send_info(self, data):
        self.data = data

    def send_ping(self):
        self.ping = True

    def tx_void(self):
        self.tx_socket.listen(1)
        while True:
            self.hdm.lg('HOST', 0, 'Ожидаю подключений...')
            connection, client_address = self.tx_socket.accept()
            try:
                self.hdm.lg('HOST', 0, 'Подключён клиент: ' + str(client_address) + ".")
                while True:
                    if self.ping:
                        start_time = time.time()
                        connection.sendall(bytes((255, 255, 255, 255, 255, 255, 255, 255)))
                        connection.recv(8)
                        self.hdm.lg('HOST', 0, "---ping took " + str((time.time() - start_time)) + " seconds ---")
                        self.ping = False
                    connection.sendall(bytes(self.data))
                    time.sleep(0.01)
            except Exception as e:
                self.hdm.lg('HOST', 1, 'Ошибка подключения или передачи: ' + str(e))
            time.sleep(1)
