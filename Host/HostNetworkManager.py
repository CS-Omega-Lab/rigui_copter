import socket
import time
import json
from threading import Thread

from Common.ConstStorage import ConstStorage as CS


class NetworkDataClient:
    def __init__(self, hdm):
        self.config = hdm.config
        self.hdm = hdm
        self.lgm = hdm.lgm
        self.remote_address = hdm.remote_address
        self.data_port = int(self.config['network']['data_port'])
        self.data = [
            CS.MID_VAL,  # Канал X
            CS.MID_VAL,  # Канал Y
            CS.MID_VAL,  # Канал Z
            CS.MID_VAL,  # Канал YAW
            CS.MID_VAL,  # Блок моторов
            CS.MIN_VAL  # Режим
        ]
        self.tx_thread = Thread(target=self.tx_void, daemon=True, args=())
        self.tx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        self.lgm.dlg('HOST', 3, '[TX] Подключаюсь к сокету: ' + str((self.remote_address, self.data_port)))
        try:
            self.tx_socket.connect((self.remote_address, self.data_port))
        except Exception as e:
            self.lgm.dlg('HOST', 1, '[TX] Ошибка подключения к сокету: ' + str(e))
            self.hdm.lg('HOST', 1, '[TX] Ошибка подключения к сокету: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.tx_thread.start()
            self.hdm.lg('HOST', 0,
                        '[TX] Подключение к ' + str((self.remote_address, self.data_port)) + ': успешно.')
        else:
            self.hdm.set_boot_lock()
        return self

    def send_info(self, data):
        self.data = data

    def tx_void(self):
        try:
            while True:
                self.tx_socket.sendall(json.dumps(self.data).encode('utf-8'))
                time.sleep(0.001)
        except Exception as e:
            self.hdm.lg('HOST', 1, '[TX] Ошибка подключения или передачи: ' + str(e))
        time.sleep(1)


class NetworkCommandClient:
    def __init__(self, hdm):
        self.config = hdm.config
        self.hdm = hdm
        self.lgm = hdm.lgm
        self.command = 2
        self.remote_address = hdm.remote_address
        self.command_port = int(self.config['network']['command_port'])
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
        self.lgm.dlg('HOST', 3, '[MX] Подключаюсь к сокету: ' + str((self.remote_address, self.command_port)))
        try:
            self.mx_socket.connect((self.remote_address, self.command_port))
        except Exception as e:
            self.lgm.dlg('HOST', 1, '[MX] Ошибка подключения к сокету: ' + str(e))
            self.hdm.lg('HOST', 1, '[MX] Ошибка подключения к сокету: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.mx_thread.start()
            self.hdm.lg('HOST', 0,
                        '[MX] Подключение к ' + str((self.remote_address, self.command_port)) + ': успешно.')
        else:
            self.hdm.set_boot_lock()
        return self

    def send_command(self, data):
        self.command = data

    def get_telemetry(self):
        return self.telemetry

    def print_init_info(self, data):
        if data[0] == 1:
            self.hdm.lg('ROBOT', 0,
                        'Камера по адресу ' + self.config['devices'][
                            'video_dev'] + ' подключена.')
        else:
            self.hdm.lg('ROBOT', 1,
                        'Камера по адресу ' + self.config['devices'][
                            'video_dev'] + ' не подключена (code: ' + str(data[0]) + ').')

        self.hdm.lg('ROBOT', 0, 'Робот готов.')

    def mx_void(self):
        try:
            while True:
                if self.command == 1:
                    self.mx_socket.sendall(bytes([1]))
                    data = self.mx_socket.recv(5)
                    self.telemetry = list(data)
                if self.command == 2:
                    time.sleep(1)
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
