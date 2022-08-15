import socket
import time
from threading import Thread


class NetworkDataClient:
    def __init__(self, hdm):
        self.config = hdm.config
        self.hdm = hdm
        self.data = []
        self.tx_thread = Thread(target=self.tx_void, daemon=True, args=())
        self.tx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        try:
            self.tx_socket.bind((self.config['network']['host'], int(self.config['network']['data_port'])))
        except Exception as e:
            self.hdm.lg('HOST', 1, '[TX] Ошибка привязки сокета: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.tx_thread.start()
            self.hdm.lg('HOST', 0, '[TX] Запуск сокета (' + self.config['network']['data_port'] + '): успешно.')
        return self

    def send_info(self, data):
        self.data = data

    def tx_void(self):
        self.tx_socket.listen(1)
        while True:
            self.hdm.lg('HOST', 0, '[TX] Ожидаю подключений...')
            connection, client_address = self.tx_socket.accept()
            try:
                self.hdm.lg('HOST', 0, '[TX] Подключён клиент: ' + str(client_address) + ".")
                while True:
                    connection.sendall(bytes((self.data[0][0], self.data[0][1], self.data[1][0], self.data[1][1],
                                              self.data[2][0], self.data[2][1], self.data[2][2], self.data[3][0],
                                              self.data[3][1])))
                    time.sleep(0.01)
            except Exception as e:
                self.hdm.lg('HOST', 1, '[TX] Ошибка подключения или передачи: ' + str(e))
            time.sleep(1)


class NetworkCommandClient:
    def __init__(self, hdm):
        self.config = hdm.config
        self.hdm = hdm
        self.command = 2
        self.telemetry = [
            '-',  # Уровень сигнала
            '-',  # Пинг
            '-',  # Заряд аккумулятора
            '-',  # Температура
            '-'  # Ток
        ]
        self.mx_thread = Thread(target=self.mx_void, daemon=True, args=())
        self.mx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        try:
            self.mx_socket.bind((self.config['network']['host'], int(self.config['network']['command_port'])))
        except Exception as e:
            self.hdm.lg('HOST', 1, '[MX] Ошибка привязки сокета: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.mx_thread.start()
            self.hdm.lg('HOST', 0, '[MX] Запуск сокета (' + self.config['network']['command_port'] + '): успешно.')
        return self

    def send_command(self, data):
        self.command = data

    def get_telemetry(self):
        return self.telemetry

    def print_init_info(self, data):
        if data[0] == 1:
            self.hdm.lg('ROBOT', 0,
                        'Камера по адресу ' + self.config['devices'][
                            'video_dev_0'] + ' подключена.')
        else:
            self.hdm.lg('ROBOT', 1,
                        'Камера по адресу ' + self.config['devices'][
                            'video_dev_0'] + ' не подключена (code: ' + str(data[0]) + ').')
        if data[2] == 1:
            self.hdm.lg('ROBOT', 0,
                        'Устройство UART-TTL на ' + self.config['devices'][
                            'uart-ttl_dev'] + ' подключено.')
        else:
            self.hdm.lg('ROBOT', 1,
                        'Устройство UART-TTL на ' + self.config['devices'][
                            'uart-ttl_dev'] + ' не подключено (code: ' + str(data[2]) + ').')

        self.hdm.lg('ROBOT', 0, 'Робот готов.')

    def mx_void(self):
        self.mx_socket.listen(1)
        while True:
            self.hdm.lg('HOST', 0, '[MX] Ожидаю подключений...')
            connection, client_address = self.mx_socket.accept()
            try:
                self.hdm.lg('HOST', 0, '[MX] Подключён клиент: ' + str(client_address) + ".")
                while True:
                    if self.command == 1:
                        connection.sendall(bytes([1]))
                        data = connection.recv(5)
                        self.telemetry = list(data)
                    if self.command == 2:
                        connection.sendall(bytes([2]))
                        data = connection.recv(3)
                        data = list(data)
                        self.print_init_info(data)
                        self.command = 1
                    time.sleep(0.2)
            except Exception as e:
                self.hdm.lg('HOST', 1, '[MX] Ошибка подключения или передачи: ' + str(e))
                self.command = 2
                self.telemetry = [
                    '-',  # Уровень сигнала
                    '-',  # Пинг
                    '-',  # Заряд аккумулятора
                    '-',  # Температура
                    '-'  # Ток
                ]
            time.sleep(1)
