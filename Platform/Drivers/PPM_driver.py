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
            self.rdm.update_init_data(1, 1)
            self.ser = serial.Serial(rdm.devices['platform_ttl_ppm_dev'], int(rdm.devices['platform_serial_speed']))
            self.data = b'[127, 127, 127, 0, 0, 0, 0, 0]'
            self.thread = Thread(target=self.roll, daemon=True, args=())

    def start(self):
        if self.available:
            self.thread.start()
        return self

    def roll(self):
        if self.available:
            while True:
                time.sleep(0.02)
                self.ser.write(self.data)

    def send(self, data):
        self.data = data

