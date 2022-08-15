import time
# noinspection PyUnresolvedReferences
# from RPi import GPIO
from threading import Thread

from Robot.CameraStreamer import CameraStreamer
from Robot.RobotNetworkManager import NetworkDataClient
from Robot.RobotNetworkManager import NetworkCommandClient
from Robot.TelemetryManager import TelemetryManager
from Robot.Drivers.BLDC import BLDC
from Robot.Drivers.ILYUSHA import ILYUSHA
from Robot.Drivers.SERVO import SERVO
from Robot.Drivers.DCMOTOR import DCMOTOR

from rich.console import Console


class DataManager:
    def __init__(self, config):
        self.config = config
        self.telemetry = []
        self.init_data = [
            0,
            0
        ]

        self.motors_summary = 0

        self.cls = Console()
        self.data_client = NetworkDataClient(self)
        self.command_client = NetworkCommandClient(self)

        self.telemetry_manager = TelemetryManager(self).start()

        self.devices = config['devices']

        self.left_motor = BLDC(self.devices['left_motor'])
        self.right_motor = BLDC(self.devices['right_motor'])
        #
        self.front_motor = DCMOTOR(self.devices['front_motor_0'], self.devices['front_motor_1'])
        self.rear_motor = DCMOTOR(self.devices['rear_motor_0'], self.devices['rear_motor_1'])

        self.first_axis = ILYUSHA(self, self.devices['first_axis'])
        self.second_axis = ILYUSHA(self, self.devices['second_axis'])
        self.third_axis = SERVO(self.devices['third_axis'])
        self.fourth_axis = DCMOTOR(self.devices['fourth_axis_0'], self.devices['fourth_axis_1'])

        self.camera_x = SERVO(self.devices['camera_x'])
        self.camera_y = SERVO(self.devices['camera_y'])

        self.camera_streamer = CameraStreamer(self, 0).start()

        self.thread = Thread(target=self.operate, daemon=True, args=())

    def start(self):
        self.data_client.start()
        self.command_client.start()
        self.thread.start()
        return self

    def update_init_data(self, key, val):
        self.init_data[key] = val

    def get_init_data(self):
        return self.init_data

    def get_motors_summary(self):
        return self.motors_summary

    def operate(self):
        time.sleep(2)
        while True:
            time.sleep(0.01)
            self.command_client.send_telemetry(self.telemetry_manager.get_telemetry())
            data = self.data_client.receive()
            self.motors_summary = abs(data[0] - 127) + abs(data[1] - 127) + abs(data[2] - 127) + abs(data[3] - 127)
            self.left_motor.move(data[1])
            self.right_motor.move(data[0])
            self.front_motor.move(data[2])
            self.rear_motor.move(data[3])
            self.first_axis.move(data[4])
            self.second_axis.move(data[4])
            self.third_axis.move(data[6])
            self.fourth_axis.move(data[5])
            self.camera_x.move(data[7])
            self.camera_y.move(data[8])

    def lg(self, src, typ, message):
        if typ == 0:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][white bold]INFO[/][red bold]::[/]" + message)
        elif typ == 1:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][red bold]ERROR[/][red bold]::[/]" + message)
        else:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][yellow bold]WARN[/][red bold]::[/]" + message)
