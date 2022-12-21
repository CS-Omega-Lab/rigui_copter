import time
from threading import Thread

from Controller.NetworkManager import NetworkDataClient
from Controller.NetworkManager import NetworkCommandClient
from Controller.Drivers.FSManager import FSManager
from Controller.Drivers.VideoReceiver import VideoReceiver
from Common.AddressManager import AddressManager
from Common.ConstStorage import ConstStorage as CS


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

        self.remote_address = None

        self.data = [
            CS.MID_VAL,  # Roll
            CS.MID_VAL,  # Pitch
            CS.MID_VAL,  # Yaw
            CS.MIN_VAL,  # Throttle
            CS.MIN_VAL,  # ArmDisarm
            CS.MIN_VAL,  # T2
            CS.MIN_VAL,  # FlightMode
            CS.MIN_VAL   # T4
        ]

        self.telemetry = [
            '-',  # Пинг
            '-',  # Ошибки
        ]

        self.thread = Thread(target=self.update, daemon=True, args=())

        self.input_manager = FSManager(self).start()

        self.get_addresses()
        if self.remote_address:
            self.data_client = NetworkDataClient(self).start()
            self.command_client = NetworkCommandClient(self).start()
        self.camera_reader = VideoReceiver(self).start()

    def set_boot_lock(self):
        self.boot_lock = True

    def in_waiting(self):
        return self.waiting

    def get_logs(self):
        return self.log_list

    def get_vals(self):
        return self.data

    def get_telemetry(self):
        return self.telemetry

    def get_addresses(self):
        am = AddressManager(self.lgm, self.config)
        remote_address = am.get_remote_address_by_name("rpi")
        if remote_address:
            self.remote_address = remote_address
        else:
            self.set_boot_lock()

    def start(self):
        time.sleep(1)
        try:
            if not self.boot_lock:
                self.thread.start()
                self.lg('CNTR', 0, 'Запуск DataManager: успешно.')
                self.waiting = False
            else:
                self.lgm.dlg('CNTR', 1, 'Ошибка запуска DataManager: boot_lock. Запуск невозможен.')
        except Exception as e:
            self.lg('CNTR', 1, 'Ошибка запуска DataManager: ' + str(e))
        return self

    def update(self):
        while True:
            time.sleep(0.001)
            self.telemetry = self.command_client.get_telemetry()
            self.data = self.input_manager.get_vals()
            self.data_client.send_info(self.data)

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
