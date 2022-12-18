import os
from threading import Thread

# noinspection PyUnresolvedReferences
import serial
import time


class PPM:
    def __init__(self, rdm):
        self.rdm = rdm
        self.available = True
        if not os.path.exists(rdm.devices['platform_ttl_ppm_dev']):
            self.rdm.lgm.dlg('PLTF', 1, 'Устройство TTL-PPM на ' + rdm.devices['platform_ttl_ppm_dev'] + ' не подключено.')
            self.rdm.update_init_data(1, 2)
            self.available = False
        else:
            self.rdm.lgm.dlg('PLTF', 0, 'Устройство TTL-PPM на ' + rdm.devices['platform_ttl_ppm_dev'] + ' подключено.')
            self.ser = serial.Serial(rdm.devices['platform_ttl_ppm_dev'], 9600)
            self.channels = [127, 127, 127, 127, 127, 127, 127, 127]
            self.next_channels = [127, 127, 127, 127, 127, 127, 127, 127]
            self.thread = Thread(target=self.roll, daemon=True, args=())

    def start(self):
        if self.available:
            self.thread.start()
        return self

    def roll(self):
        if self.available:
            while True:
                time.sleep(0.01)
                self.ser.write(bytes([255]))
                for i in range(len(self.channels)):
                    self.ser.write(bytes([self.channels[i]]))
                self.channels = self.next_channels

    def send(self, new_channels):
        new = new_channels
        if not(len(new) == 8):
            self.rdm.lgm.dlg('PLTF', 1, 'Неверная длина массива передачи.')
        self.next_channels = new

