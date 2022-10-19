import time
from threading import Thread

from Host.HostNetworkManager import NetworkDataClient
from Host.HostNetworkManager import NetworkCommandClient
# from Host.Drivers.KeyManager import KeyManager
from Host.Drivers.GPManager import GPManager
from Host.CameraReader import CameraReader


class DataManager:
    def __init__(self, config, rows):
        self.log_list = ''''''
        self.log_ctr = 0
        self.rows = rows
        self.config = config
        self.init_passed = False

        self.mode = [
            127  # Текущая максимальная скорость
        ]

        self.vals = [
            (127, 127),  # Состояние двигателей гусениц
            (127, 127),  # Состояние двигателей плавников
            (127, 127, 127, 127),  # Состояние двигателей осей
            (127, 127)  # Параметры двигателей подвеса камеры
        ]

        self.telemetry = [
            '-',  # Уровень сигнала
            '-',  # Пинг
            '-',  # Заряд аккумулятора
            '-',  # Температура
            '-'   # Ток
        ]

        self.thread = Thread(target=self.update, daemon=True, args=())
        # self.keyboard_manager = KeyManager(self).start()
        self.gamepad_manager = GPManager(self).start()
        self.data_client = NetworkDataClient(self).start()
        self.command_client = NetworkCommandClient(self).start()
        self.camera_reader = CameraReader(self).start()

    def get_logs(self):
        return self.log_list

    def get_mode(self):
        return self.mode

    def get_vals(self):
        return self.vals

    def get_telemetry(self):
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
            self.telemetry = self.command_client.get_telemetry()
            self.mode = self.gamepad_manager.get_mode()
            self.vals = self.gamepad_manager.get_vals()
            self.data_client.send_info(self.vals)
