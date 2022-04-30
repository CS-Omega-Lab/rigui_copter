import time
# noinspection PyUnresolvedReferences
from RPi import GPIO
from threading import Thread

from Robot.RobotNetworkClient import NetworkClient as NC
from Robot.Drivers.BLDC import BLDC
from Robot.Drivers.ILYUSHA import ILYUSHA
from Robot.Drivers.SERVO import SERVO
from Robot.Drivers.DCMOTOR import DCMOTOR

from rich.console import Console


class DataManager:
    def __init__(self, config):
        self.config = config

        self.cls = Console()
        self.nc = NC(self)
        devices = config['devices']

        self.left_motor = BLDC(devices['left_motor'])
        self.right_motor = BLDC(devices['left_motor'])

        self.front_motor = DCMOTOR(devices['front_motor_0'], devices['front_motor_1'])
        self.rear_motor = DCMOTOR(devices['rear_motor_0'], devices['rear_motor_1'])

        self.first_axis = ILYUSHA(self, devices['first_axis'])
        self.second_axis = ILYUSHA(self, devices['second_axis'])
        self.third_axis = SERVO(devices['third_axis'])
        self.fourth_axis = DCMOTOR(devices['fourth_axis_0'], devices['fourth_axis_1'])

        self.camera_x = SERVO(devices['camera_x'])
        self.camera_y = SERVO(devices['camera_y'])

        self.thread = Thread(target=self.operate, daemon=True, args=())

    def instance(self):
        return self

    def start(self):
        self.nc.start()
        self.thread.start()
        return self

    def operate(self):
        time.sleep(2)
        while True:
            time.sleep(0.01)
            cmd = self.nc.receive()
            self.left_motor.move(cmd[0])
            self.right_motor.changeSpeed(cmd[1])
            self.front_motor.move(cmd[2])
            self.rear_motor.move(cmd[3])
            if cmd[4] == 0:
                self.first_axis.move(cmd[5])
            if cmd[4] == 1:
                self.second_axis.move(cmd[5])
            if cmd[4] == 2:
                self.third_axis.move(cmd[5])
            if cmd[4] == 3:
                self.fourth_axis.move(cmd[5])
            self.camera_x.move(cmd[6])
            self.camera_y.move(cmd[7])

    def lg(self, src, typ, message):
        if typ == 0:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][white bold]INFO[/][red bold]::[/]" + message)
        elif typ == 1:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][red bold]ERROR[/][red bold]::[/]" + message)
        else:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][yellow bold]WARN[/][red bold]::[/]" + message)
