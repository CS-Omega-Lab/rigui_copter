from threading import Thread

# noinspection PyUnresolvedReferences
import RPi.GPIO as gpio
# noinspection PyUnresolvedReferences
import serial
import time


class WrongMassiveSize(Exception):
    pass


class PPM:

    def __init__(self):
        self.ser = serial.Serial("/dev/ttyUSB0", 9600)
        self.channels = [127, 127, 127, 127, 127, 127, 127, 127]
        self.next_channels = [127, 127, 127, 127, 127, 127, 127, 127]
        self.thread = Thread(target=self.roll, daemon=True, args=())

    def start(self):
        self.thread.start()
        return self

    def roll(self):
        while True:
            time.sleep(0.01)
            self.ser.write(bytes([255]))
            for i in range(len(self.channels)):
                self.ser.write(bytes([self.channels[i]]))
            self.channels = self.next_channels

    def send(self, new_channels):
        new = new_channels
        if not(len(new) == 8):
            raise WrongMassiveSize("бан по причине пидорас, неправильный размер массива")
        pass
        self.next_channels = new

