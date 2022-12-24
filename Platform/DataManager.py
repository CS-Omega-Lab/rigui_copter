import time
from threading import Thread

from Platform.Drivers.VideoSender import VideoStreamer
from Platform.NetworkManager import NetworkDataClient
from Platform.NetworkManager import NetworkCommandClient
from Platform.TelemetryManager import TelemetryManager
from Platform.Drivers.PPM_driver import PPM
from Common.AddressManager import AddressManager


class DataManager:
    def __init__(self, config, lgm):
        self.config = config
        self.telemetry = []
        self.init_data = [0,0]
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

    def stop_video_stream(self):
        self.video_streamer.stop()

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

    def set_stream_running(self):
        self.video_stream_state = True

    def lazy_process_start(self):
        while not self.remote_address:
            time.sleep(0.1)
        if not self.video_stream_state:
            self.video_streamer = VideoStreamer(self).start()
        self.telemetry_manager.start(self.remote_address)

    def operate(self):
        time.sleep(1)
        self.command_client.send_telemetry(self.telemetry_manager.get_telemetry())
        while True:
            time.sleep(0.001)
            self.command_client.send_telemetry(self.telemetry_manager.get_telemetry())
            self.copter_bus.send(self.data_client.receive())
