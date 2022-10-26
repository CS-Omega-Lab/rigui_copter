import time
from threading import Thread

from Host.HostNetworkManager import NetworkDataClient
from Host.HostNetworkManager import NetworkCommandClient
from Host.Drivers.KeyManager import KeyManager
from Host.Drivers.GPManager import GPManager
from Host.CameraReader import CameraReader
from Common.AddressManager import AddressManager

from netifaces import interfaces, ifaddresses, AF_INET
import socket


class DataManager:
    def __init__(self, config, lgm, rows):
        self.log_list = ''''''
        self.log_ctr = 0
        self.rows = rows
        self.config = config
        self.lgm = lgm
        self.init_passed = False
        self.waiting = True
        self.boot_lock = False

        self.local_address = None
        self.remote_address = None

        self.vals = [
            (127, 127),             # Состояние двигателей гусениц
            (127, 127),             # Состояние двигателей плавников
            (127, 127, 127, 127),   # Состояние двигателей осей
            (127, 127)              # Параметры двигателей подвеса камеры
        ]

        self.telemetry = [
            '-',  # Уровень сигнала
            '-',  # Пинг
            '-',  # Заряд аккумулятора
            '-',  # Температура
            '-'   # Ток
        ]

        self.thread = Thread(target=self.update, daemon=True, args=())

        if config['general']['control'] == "gamepad":
            self.input_manager = GPManager(self).start()
        elif config['general']['control'] == "keyboard":
            self.keyboard_manager = KeyManager(self).start()
        else:
            self.lgm.dlg('HOST', 1, 'Неизвестный способ ввода: '+str(config['general']['control']))
            self.boot_lock = True

        self.get_addresses()
        if self.remote_address:
            self.data_client = NetworkDataClient(self).start()
            self.command_client = NetworkCommandClient(self).start()
        self.camera_reader = CameraReader(self).start()
        time.sleep(2)

    def set_boot_lock(self):
        self.boot_lock = True

    def in_waiting(self):
        return self.waiting

    def get_logs(self):
        return self.log_list

    def get_vals(self):
        return self.vals

    def get_telemetry(self):
        return self.telemetry

    def get_addresses(self):
        am = AddressManager(self.lgm)
        subnet = str(self.config['network']['subnet'])
        local_address = am.get_local_address_by_subnet(subnet)
        remote_address = am.get_remote_address_by_name("rpi.local")

        if local_address:
            self.local_address = local_address
        else:
            self.set_boot_lock()

        if remote_address:
            self.remote_address = remote_address
        else:
            self.set_boot_lock()

    def start(self):
        try:
            if not self.boot_lock:
                self.thread.start()
                self.lg('HOST', 0, 'Запуск DataManager: успешно.')
                self.waiting = False
            else:
                self.lgm.dlg('HOST', 1, 'Ошибка запуска DataManager: boot_lock. Запуск невозможен.')
        except Exception as e:
            self.lg('HOST', 1, 'Ошибка запуска DataManager: ' + str(e))
        return self

    def update(self):
        while True:
            time.sleep(0.01)
            self.telemetry = self.command_client.get_telemetry()
            self.vals = self.input_manager.get_vals()
            self.data_client.send_info(self.vals)

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
