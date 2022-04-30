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
            True,   # Режим управления: ручной (True) или полуавтомат (False)
            True,   # Режим передачи данных для ручного режима: езда (True) или манипулятор (False)
            100,    # Текущая максимальная скорость
            0,      # Номер пресета
            1,      # Длительность пресета
            False   # PING
        ]

        self.vals = [
            (127, 127),  # Состояние двигателей гусениц
            (127, 127),  # Состояние двигателей плавников
            0,           # Текущая ось (для манипулятора)
            127,         # Состояние двигателя оси (для манипулятора)
            (127, 127)   # Параметры двигателей подвеса камеры
        ]

        self.thread = Thread(target=self.update, daemon=True, args=())
        self.keyboard_connector = KeyManager(self).start()
        self.network_client = NetworkClient(self, config['general']).start()
        self.camera_reader = ManualCameraReader(self).start()

    def get_logs(self):
        return self.log_list

    def get_mode(self):
        return self.mode

    def get_vals(self):
        return self.vals

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
        if self.log_ctr >= self.rows - 4:
            idx = self.log_list.find('\r\n')
            self.log_list = self.log_list[idx + 1:]

    def start(self):
        try:
            self.thread.start()
            self.lg('HOST', 0, 'Запуск DataManager: успешно.')
        except Exception as e:
            self.lg('HOST', 1, 'Ошибка запуска DataManager: '+str(e))
        return self

    def update(self):
        while True:
            time.sleep(0.01)
            self.mode = self.keyboard_connector.get_mode()
            self.vals = self.keyboard_connector.get_vals()
            if self.mode[5]:
                self.network_client.send_ping()
                continue
            self.network_client.send_info(self.vals)
