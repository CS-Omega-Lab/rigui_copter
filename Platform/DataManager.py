import time
from threading import Thread

from Platform.Drivers.VideoStreamer import VideoStreamer
from Platform.QReader import QReader
from Platform.NetworkManager import NetworkDataClient
from Platform.NetworkManager import NetworkCommandClient
from Platform.TelemetryManager import TelemetryManager
from Platform.Drivers.PPM_driver import PPM
from Common.AddressManager import AddressManager
from Common.ConstStorage import ConstStorage as CS


class DataManager:
    def __init__(self, config, lgm, mode=True):
        self.config = config
        self.mode = mode
        self.telemetry = []
        self.init_data = [
            0,
            0
        ]
        self.motors_summary = 0
        self.lgm = lgm
        self.local_address = None
        self.remote_address = None
        self.boot_lock = False
        self.video_stream_state = False
        self.devices = config['devices']

        self.get_addresses()

        self.data_client = NetworkDataClient(self, self.lgm)
        self.command_client = NetworkCommandClient(self, self.lgm)
        self.telemetry_manager = TelemetryManager(self, self.lgm)

        if not self.boot_lock:
            self.copter_bus = PPM(self).start()
            self.thread = Thread(target=self.operate, daemon=True, args=())
            self.qr_reader = None
            self.video_streamer = None
        else:
            self.lgm.dlg('PLTF', 1, 'Ошибка запуска DataManager: boot_lock. Запуск невозможен.')

    def start(self):
        if not self.boot_lock:
            self.data_client.start()
            self.command_client.start()
            self.thread.start()
        return self

    def set_boot_lock(self):
        self.boot_lock = True

    def drop_remote_address(self):
        self.remote_address = None

    def set_remote_address(self, remote):
        self.remote_address = remote

    def get_addresses(self):
        am = AddressManager(self.lgm, self.config)
        local_address = am.get_local_address_by_subnet()

        if local_address:
            self.local_address = local_address
        else:
            self.set_boot_lock()

    def update_init_data(self, key, val):
        self.init_data[key] = val

    def get_init_data(self):
        return self.init_data

    def get_motors_summary(self):
        return self.motors_summary

    def lazy_process_start(self):
        time.sleep(2)
        while not self.remote_address:
            time.sleep(1)
        if self.mode:
            self.video_streamer = VideoStreamer(self).start()
        else:
            self.qr_reader = QReader(self).start()
        self.telemetry_manager.start(self.remote_address)

    def operate(self):
        time.sleep(2)
        while True:
            time.sleep(0.001)
            self.command_client.send_telemetry(self.telemetry_manager.get_telemetry())
            data = self.data_client.receive()
            self.motors_summary = int((abs(data[0] - CS.MID_VAL) + abs(data[1] - CS.MID_VAL) + abs(
                data[2]) + abs(data[3] - CS.MID_VAL))/16)
            self.copter_bus.send([
                int(data[0]/16),
                int(data[1]/16),
                int(data[2]/16),
                int(data[3]/16),
                int(data[4]/16),
                int(data[5]/16),
                127,
                127,
            ])
