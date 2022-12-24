import socket
import time
from threading import Thread

from Common.ConstStorage import ConstStorage as CS


class NetworkDataClient:
    def __init__(self, rdm, lgm):
        self.net_config = rdm.config['network']
        self.rdm = rdm
        self.lgm = lgm
        self.local_address = rdm.local_address
        self.rx_buf = b''
        self.last_cmd = [
            CS.MID_VAL,  # Roll
            CS.MID_VAL,  # Pitch
            CS.MID_VAL,  # Yaw
            CS.MIN_VAL,  # Throttle
            CS.MIN_VAL,  # T1
            CS.MIN_VAL,  # T2
            CS.MIN_VAL,  # T3
            CS.MIN_VAL  # T4
        ]
        self.rx_thread = Thread(target=self.rx_void, daemon=True, args=())
        self.decode_thread = Thread(target=self.decode_void, daemon=True, args=())
        self.rx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        self.lgm.dlg('PLTF', 3,
                     '[RX] Открываю сокет: ' + str((self.local_address, int(self.net_config['platform_data_port']))))
        try:
            self.rx_socket.bind((self.local_address, int(self.net_config['platform_data_port'])))
            self.lgm.dlg('PLTF', 3,
                         '[RX] Сокет открыт: ' + str((self.local_address, int(self.net_config['platform_data_port']))))
        except Exception as e:
            self.lgm.dlg('PLTF', 1, '[RX] Ошибка привязки сокета: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.rx_thread.start()
            self.decode_thread.start()

    def receive(self):
        return self.last_cmd

    def decode_void(self):
        while True:
            time.sleep(0.001)
            cp = self.rx_buf
            m_v1 = cp.find(b'\x5b')
            m_v2 = cp.find(b'\x5d')
            if m_v1 != -1 and m_v2 != -1:
                # self.last_cmd = list(json.loads(cp[m_v1:m_v2 + 1].decode('utf-8')))
                self.last_cmd = cp[m_v1:m_v2 + 1]
                self.rx_buf = self.rx_buf[m_v2 + 1:len(self.rx_buf)]

    def rx_void(self):
        self.rx_socket.listen(1)
        while True:
            self.lgm.dlg('PLTF', 0, '[RX] Ожидаю подключений...')
            connection, client_address = self.rx_socket.accept()
            try:
                self.lgm.dlg('PLTF', 0, '[RX] Подключён клиент: ' + str(client_address) + ".")
                self.rdm.set_remote_address(str(client_address[0]))
                self.rdm.lazy_process_start()
                while True:
                    data = connection.recv(64)
                    self.rx_buf += data
                    time.sleep(0.001)
            except Exception as e:
                self.lgm.dlg('PLTF', 1, '[RX] Ошибка подключения или передачи: ' + str(e))
                self.rdm.drop_remote_address()
                self.rdm.stop_video_stream()
                self.rx_buf = b''
                time.sleep(0.1)
                self.last_cmd = [
                    CS.MIN_VAL,  # Roll
                    CS.MIN_VAL,  # Pitch
                    CS.MIN_VAL,  # Yaw
                    CS.MIN_VAL,  # Throttle
                    CS.MIN_VAL,  # T1
                    CS.MIN_VAL,  # T2
                    CS.MIN_VAL,  # T3
                    CS.MIN_VAL  # T4
                ]
            time.sleep(0.5)


class NetworkCommandClient:
    def __init__(self, rdm, lgm):
        self.net_config = rdm.config['network']
        self.rdm = rdm
        self.lgm = lgm
        self.telemetry = []
        self.local_address = rdm.local_address
        self.mx_thread = Thread(target=self.mx_void, daemon=True, args=())
        self.mx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        self.lgm.dlg('PLTF', 3,
                     '[MX] Открываю сокет: ' + str((self.local_address, int(self.net_config['platform_command_port']))))
        try:
            self.mx_socket.bind((self.local_address, int(self.net_config['platform_command_port'])))
            self.lgm.dlg('PLTF', 3,
                         '[MX] Сокет открыт: ' + str(
                             (self.local_address, int(self.net_config['platform_command_port']))))
        except Exception as e:
            self.lgm.dlg('PLTF', 1, '[MX] Ошибка привязки сокета: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.mx_thread.start()

    def send_telemetry(self, data):
        self.telemetry = data

    def mx_void(self):
        self.mx_socket.listen(1)
        while True:
            self.lgm.dlg('PLTF', 0, '[MX] Ожидаю подключений...')
            connection, client_address = self.mx_socket.accept()
            try:
                self.lgm.dlg('PLTF', 0, '[MX] Подключён клиент: ' + str(client_address) + ".")
                while True:
                    data = connection.recv(1)
                    command = list(data)
                    if command[0] == 2:
                        time.sleep(1)
                        connection.sendall(bytes(self.rdm.get_init_data()))
                    if command[0] == 1:
                        connection.sendall(bytes(self.telemetry))
                    time.sleep(0.4)
            except Exception as e:
                self.lgm.dlg('PLTF', 1, '[MX] Ошибка подключения или передачи: ' + str(e))
                self.rdm.drop_remote_address()
                self.rdm.stop_video_stream()
            time.sleep(0.5)
