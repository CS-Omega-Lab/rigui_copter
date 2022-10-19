import socket
import time
from threading import Thread


class NetworkDataClient:
    def __init__(self, hdm):
        self.config = hdm.config
        self.hdm = hdm
        self.data = [
            (127, 127),  # Состояние двигателей гусениц
            (127, 127),  # Состояние двигателей плавников
            (127, 127, 127, 127),  # Состояние двигателей осей
            (127, 127)  # Параметры двигателей подвеса камеры
        ]
        self.tx_thread = Thread(target=self.tx_void, daemon=True, args=())
        self.tx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        try:
            self.tx_socket.connect((self.config['network']['host'], int(self.config['network']['data_port'])))
        except Exception as e:
            self.hdm.lg('HOST', 1, '[TX] Ошибка подключения к сокету: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.tx_thread.start()
            self.hdm.lg('HOST', 0, '[TX] Подключение к сокету (' + self.config['network']['data_port'] + '): успешно.')
        return self

    def send_info(self, data):
        self.data = data

    def tx_void(self):
        try:
            while True:
                self.tx_socket.sendall(bytes((self.data[0][0], self.data[0][1], self.data[1][0], self.data[1][1],
                                              self.data[2][0], self.data[2][1], self.data[2][2], self.data[2][3],
                                              self.data[3][0], self.data[3][1])))
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
            self.mx_socket.connect((self.config['network']['host'], int(self.config['network']['command_port'])))
        except Exception as e:
            self.hdm.lg('HOST', 1, '[TX] Ошибка подключения к сокету: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.mx_thread.start()
            self.hdm.lg('HOST', 0, '[MX] Подключение к сокету (' + self.config['network']['command_port'] + '): успешно.')
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
        if data[1] == 1:
            self.hdm.lg('ROBOT', 0,
                        'Устройство UART-TTL на ' + self.config['devices'][
                            'uart-ttl_dev'] + ' подключено.')
        else:
            self.hdm.lg('ROBOT', 1,
                        'Устройство UART-TTL на ' + self.config['devices'][
                            'uart-ttl_dev'] + ' не подключено (code: ' + str(data[1]) + ').')

        self.hdm.lg('ROBOT', 0, 'Робот готов.')

    def mx_void(self):
        try:
            while True:
                if self.command == 1:
                    self.mx_socket.sendall(bytes([1]))
                    data = self.mx_socket.recv(5)
                    self.telemetry = list(data)
                if self.command == 2:
                    self.mx_socket.sendall(bytes([2]))
                    data = self.mx_socket.recv(3)
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
