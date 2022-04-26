import time
from RPi import GPIO
from threading import Thread

from Robot.RobotNetworkClient import NetworkClient as NC
from Robot.Drivers.BLDC import BLDC
from Robot.Drivers.ILYUSHA import ILYUSHA
from Robot.Drivers.SERVO import SERVO
from Robot.Drivers.DCMOTOR import DCMOTOR

from rich.console import Console


class DataProvider:
    def __init__(self):
        self.cls = Console()
        self.nc = NC()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        self.left_bldc = BLDC(33)
        # self.right_bldc = BLDC(33)

        # self.front_fin = DCMOTOR()
        # self.rear_fin = DCMOTOR()

        self.first_axis = ILYUSHA(1)
        self.second_axis = ILYUSHA(2)
        self.third_axis = SERVO(31)
        self.fourth_axis = DCMOTOR(29, 32)

        self.thread = Thread(target=self.operate, daemon=True, args=())

    def instance(self):
        return self

    def start(self):
        self.nc.start()
        self.thread.start()
        time.sleep(0.05)
        self.left_bldc.move(255)
        time.sleep(0.05)
        self.left_bldc.move(127)
        return self

    def operate(self):
        time.sleep(2)
        while True:
            time.sleep(0.01)
            cmd = self.nc.receive()
            if cmd[0]:
                self.left_bldc.move(cmd[1])
                # self.right_bldc.changeSpeed(cmd[2])
                # self.front_fin.move(cmd[3])
                # self.rear_fin.move(cmd[4])
            else:
                if cmd[5] == 0:
                    self.first_axis.move(cmd[6])
                if cmd[5] == 1:
                    self.second_axis.move(cmd[6])
                if cmd[5] == 2:
                    self.third_axis.move(cmd[6])
                if cmd[5] == 3:
                    self.fourth_axis.move(cmd[6])

    def lg(self, src, typ, message):
        if typ == 0:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][white bold]INFO[/][red bold]::[/]" + message)
        elif typ == 1:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][red bold]ERROR[/][red bold]::[/]" + message)
        else:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][yellow bold]WARN[/][red bold]::[/]" + message)
