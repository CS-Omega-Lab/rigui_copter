import time
# noinspection PyUnresolvedReferences
# from RPi import GPIO
from threading import Thread

from Common.AddressManager import AddressManager
from Robot.Drivers.VideoStreamer import VideoStreamer
from Robot.QReader import QReader
from Robot.RobotNetworkManager import NetworkDataClient
from Robot.RobotNetworkManager import NetworkCommandClient
from Robot.TelemetryManager import TelemetryManager
from Robot.Drivers.BLDCMotor import BLDCMOTOR
from Robot.Drivers.Ilyusha import ILYUSHA
from Robot.Drivers.Servo import SERVO
from Robot.Drivers.DCMotor import DCMOTOR


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

        self.get_addresses()

        self.data_client = NetworkDataClient(self, self.lgm)
        self.command_client = NetworkCommandClient(self, self.lgm)

        self.telemetry_manager = TelemetryManager(self, self.lgm)

        self.devices = config['devices']

        if not self.boot_lock:
            self.left_motor = BLDCMOTOR(self.devices['left_motor'], self.config, self.lgm)
            self.right_motor = BLDCMOTOR(self.devices['right_motor'], self.config, self.lgm)

            self.front_motor = DCMOTOR(self.devices['front_motor_0'], self.devices['front_motor_1'], self.lgm)
            self.rear_motor = DCMOTOR(self.devices['rear_motor_0'], self.devices['rear_motor_1'], self.lgm)

            self.first_axis = ILYUSHA(self, self.devices['first_axis'], self.lgm)
            self.second_axis = ILYUSHA(self, self.devices['second_axis'], self.lgm)
            self.third_axis = SERVO(self.devices['third_axis'], False, self.lgm)
            self.fourth_axis = DCMOTOR(self.devices['fourth_axis_0'], self.devices['fourth_axis_1'], self.lgm)

            self.camera_x = SERVO(self.devices['camera_x'], True, self.lgm)
            self.camera_y = SERVO(self.devices['camera_y'], True, self.lgm)

            self.qr_reader = None

            self.thread = Thread(target=self.operate, daemon=True, args=())

            self.video_streamer = None
        else:
            self.lgm.dlg('HOST', 1, 'Ошибка запуска DataManager: boot_lock. Запуск невозможен.')

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
        am = AddressManager(self.lgm)
        subnet = str(self.config['network']['subnet'])
        local_address = am.get_local_address_by_subnet(subnet)

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
            time.sleep(0.01)
            self.command_client.send_telemetry(self.telemetry_manager.get_telemetry())
            data = self.data_client.receive()
            self.motors_summary = abs(data[0] - 127) + abs(data[1] - 127) + abs(data[2] - 127) + abs(data[3] - 127)
            self.left_motor.move(data[0])
            self.right_motor.move(data[1])
            self.front_motor.move(data[2])
            self.rear_motor.move(data[3])
            self.first_axis.move(data[4])
            self.second_axis.move(data[5])
            self.third_axis.move(data[6])
            self.fourth_axis.move(data[7])
            self.camera_x.move(data[8])
            self.camera_y.move(data[9])
            # if data[10] > 127:
            #     if not self.video_stream_state:
            #         self.video_streamer.stop()
            #         time.sleep(2)
            #         self.qr_reader.start()
            # else:
            #     if self.video_stream_state:
            #         self.qr_reader.stop()
            #         time.sleep(2)
            #         self.video_streamer.start()

