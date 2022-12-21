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
            self.rdm.lgm.dlg('PLTF', 1,
                             'Устройство TTL-PPM на ' + rdm.devices['platform_ttl_ppm_dev'] + ' не подключено.')
            self.rdm.update_init_data(1, 2)
            self.available = False
        else:
            self.rdm.lgm.dlg('PLTF', 0, 'Устройство TTL-PPM на ' + rdm.devices['platform_ttl_ppm_dev'] + ' подключено.')
            self.rdm.update_init_data(1, 1)
            self.ser = serial.Serial(rdm.devices['platform_ttl_ppm_dev'], 115200)
            self.channels = [2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048]
            self.data = [2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048]
            self.thread = Thread(target=self.roll, daemon=True, args=())

    def start(self):
        if self.available:
            self.thread.start()
        return self

    def roll(self):
        if self.available:
            while True:
                time.sleep(0.01)
                # self.ser.write(bytes([255]))
                # for i in range(len(self.channels)):
                #     self.ser.write(bytes([self.channels[i]]))
                self.ser.write('$' + bytes([self.channels[0]]) + ' ' + bytes([self.channels[1]]) + ' ' + bytes(
                    [self.channels[2]]) + ' ' + bytes([self.channels[3]]) + ' ' + bytes(
                    [self.channels[4]]) + ' ' + bytes([self.channels[5]]) + ' ' + bytes(
                    [self.channels[6]]) + ' ' + bytes([self.channels[7]]) + ';')
                self.channels = self.data

    def send(self, data):
        # pass
        self.data = data
