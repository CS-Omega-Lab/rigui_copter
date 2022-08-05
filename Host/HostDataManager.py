import time
from threading import Thread

from Host.HostNetworkClient import NetworkClient
from Host.Drivers.KeyManager import KeyManager
from Host.ManualCameraReader import ManualCameraReader


class DataManager:
    def __init__(self, config, rows):
        self.log_list = ''''''
        self.log_ctr = 0
        self.rows = rows
        self.config = config

        self.mode = [
            100  # Текущая максимальная скорость
        ]

        self.vals = [
            (127, 127),       # Состояние двигателей гусениц
            (127, 127),       # Состояние двигателей плавников
            (127, 127, 127),  # Состояние двигателей осей
            (127, 127)        # Параметры двигателей подвеса камеры
        ]

        self.telemetry = [
            100,  # Уровень сигнала
            0.1,  # Пинг
            100,  # Заряд аккумулятора
            100,  # Температура
            100   # Ток
        ]

        self.thread = Thread(target=self.update, daemon=True, args=())
        self.keyboard_manager = KeyManager(self).start()
        self.network_client = NetworkClient(self, config['network']).start()
        # self.camera_reader = ManualCameraReader(self, config['network']['video_port_0']).start()
        # self.camera_reader = ManualCameraReader(self, config['network']['video_port_1']).start()

    def get_logs(self):
        return self.log_list

    def get_mode(self):
        return self.mode

    def get_vals(self):
        return self.vals

    def get_telemetry_data(self):
        return self.telemetry

    def lg(self, src, typ, message):
        if typ == 0:
            self.log_list += "[blue bold]\[" + src + \
                             "][/][red bold]::[/][white bold]INFO[/][red bold]::[/]" + message + "\r\n"
        elif typ == 1:
            self.log_list += "[blue bold]\[" + src + \
                             "][/][red bold]::[/][red bold]ERROR[/][red bold]::[/]" + message + "\r\n"
        else:
            self.log_list += "[blue bold]\[" + src + \
                             "][/][red bold]::[/][yellow bold]WARN[/][red bold]::[/]" + message + "\r\n"
        self.log_ctr += 1
        if self.log_ctr >= self.rows - 14:
            idx = self.log_list.find('\r\n')
            self.log_list = self.log_list[idx + 1:]

    def start(self):
        try:
            self.thread.start()
            self.lg('HOST', 0, 'Запуск DataManager: успешно.')
        except Exception as e:
            self.lg('HOST', 1, 'Ошибка запуска DataManager: ' + str(e))
        return self

    def update(self):
        while True:
            time.sleep(0.01)
            self.mode = self.keyboard_manager.get_mode()
            self.vals = self.keyboard_manager.get_vals()
            self.network_client.send_info(self.vals)
