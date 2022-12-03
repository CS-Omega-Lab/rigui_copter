import RPi.GPIO as gpio
import time


class WrongMassiveSize(Exception):
    pass

class PPM:

    def __init__(self, pin):
        self.pin = pin
        self.channels = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.pin, gpio.OUT)
        gpio.output(self.pin, gpio.LOW)
        self.pulse_width = 300
        self.next_channels = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]


    def __pulse__(self):
        gpio.output(self.pin, gpio.HIGH)
        time.sleep(self.pulse_width / 1000000)
        gpio.output(self.pin, gpio.LOW)

    def roll(self):
        for i in self.channels:
            self.__pulse__()
            time.sleep(i / 1000000)
        self.__pulse__()
        time.sleep((22500 - 9 * self.pulse_width - sum(self.channels)) / 1000000)
        self.channels = self.next_channels

    def change_channels(self, new_channels):
        new = new_channels
        if not(len(new) == 8):
            raise WrongMassiveSize("бан по причине пидорас, неправильный размер массива")
            pass
        for i in range(len(new)):
            new[i] = 500 + (new[i] / 4096) * 1000
        self.next_channels = new

if __name__ == "__main__":
    gpio.setwarnings(False)
    p = PPM(16)
    a = []
    for i in range(0, 8):
        a.append(2048)
    p.change_channels(a)
    while True:
        p.roll()