# noinspection PyUnresolvedReferences
import serial
import time
import os


class ILYUSHA:
    def __init__(self, rdm, ch_id):
        self.poss = None
        self.rdm = rdm
        self.available = False
        if not os.path.exists(rdm.devices['uart-ttl_dev']):
            rdm.lg('ROBOT', 1, 'Устройство UART-TTL на '+rdm.devices['uart-ttl_dev']+' не подключено.')
            self.rdm.update_init_data(1, 2)
        else:
            self.available = True
            self.ser = serial.Serial(rdm.devices['uart-ttl_dev'], 115200)
            rdm.lg('ROBOT', 0, 'Устройство UART-TTL на ' + rdm.devices['uart-ttl_dev'] + ' подключено.')
            self.rdm.update_init_data(1, 1)
            rdm.lg('ROBOT', 0, 'Пингую устройство UART-TTL на ' + rdm.devices['uart-ttl_dev'] + ', ID=' + ch_id + '...')
            while self.flag:
                self.ping()
                time.sleep(0.1)
            rdm.lg('ROBOT', 0, 'Устройство UART-TTL на ' + rdm.devices['uart-ttl_dev'] + ', ID=' + ch_id + ' готово.')
        self.ID = int(ch_id)
        self.flag = True
        self.velocity = 50
        self.stop_flag = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.motor_enable(0)

    def read_position(self):
        data = []
        if self.available:
            self.ser.reset_input_buffer()
            self.ser.write(bytes([255]))
            self.ser.write(bytes([255]))
            self.ser.write(bytes([self.ID]))
            self.ser.write(bytes([4]))
            self.ser.write(bytes([2]))
            self.ser.write(bytes([36]))
            self.ser.write(bytes([2]))
            self.ser.write(bytes([255 - (self.ID + 4 + 2 + 36 + 2) % 256]))
            time.sleep(0.01)
            while self.ser.in_waiting():
                data.append(self.ser.read())
            datum = None
            try:
                datum = [int.from_bytes(data[5], byteorder='big'), int.from_bytes(data[6], byteorder='big')]
            except Exception as e:
                self.rdm.lg('ROBOT', 1, 'Устройство UART-TTL не прислало данные.')
            return datum
        return []

    def move_speed(self, speed):
        if self.available:
            self.ser.reset_input_buffer()
            self.ser.write(bytes([255]))
            self.ser.write(bytes([255]))
            self.ser.write(bytes([self.ID]))
            self.ser.write(bytes([5]))
            self.ser.write(bytes([3]))
            self.ser.write(bytes([32]))
            if speed >= 0:
                self.ser.write(bytes([speed]))
                self.ser.write(bytes([0]))
                self.ser.write(bytes([255 - (self.ID + 5 + 3 + 32 + speed) % 256]))
            else:
                self.ser.write(bytes([255 + speed]))
                self.ser.write(bytes([255]))
                self.ser.write(bytes([255 - (self.ID + 5 + 3 + 32 + 255 + speed + 255) % 256]))
            time.sleep(0.01)
            while self.ser.in_waiting():
                self.ser.reset_input_buffer()

    def move_position(self, position):
        if self.available:
            self.ser.reset_input_buffer()
            self.ser.write(bytes([255]))
            self.ser.write(bytes([255]))
            self.ser.write(bytes([self.ID]))
            self.ser.write(bytes([5]))
            self.ser.write(bytes([3]))
            self.ser.write(bytes([30]))
            self.ser.write(bytes([position[0]]))
            self.ser.write(bytes([position[1]]))
            self.ser.write(bytes([255 - (self.ID + 5 + 3 + 30 + position[1] + position[0]) % 256]))
            time.sleep(0.01)
            while self.ser.in_waiting():
                self.ser.reset_input_buffer()

    def motor_enable(self, mode):
        if self.available:
            self.ser.reset_input_buffer()
            self.ser.write(bytes([255]))
            self.ser.write(bytes([255]))
            self.ser.write(bytes([self.ID]))
            self.ser.write(bytes([4]))
            self.ser.write(bytes([3]))
            self.ser.write(bytes([24]))
            self.ser.write(bytes([mode]))
            self.ser.write(bytes([255 - (self.ID + 4 + 3 + 24 + mode) % 256]))
            time.sleep(0.01)
            while self.ser.in_waiting():
                self.ser.reset_input_buffer()

    def ping(self):
        if self.available:
            self.ser.write(bytes([255]))
            self.ser.write(bytes([255]))
            self.ser.write(bytes([self.ID]))
            self.ser.write(bytes([2]))
            self.ser.write(bytes([1]))
            self.ser.write(bytes([255 - (self.ID + 2 + 1) % 256]))
            time.sleep(0.01)
            while self.ser.in_waiting():
                self.ser.reset_input_buffer()
                self.flag = False

    def move(self, speed):
        if self.available:
            self.motor_enable(2)
            if speed == 127 and not self.stop_flag:
                self.motor_enable(1)
                pos = self.read_position()
                if pos is not None:
                    self.poss = pos
                self.move_position(self.poss)
            elif speed > 127:
                self.move_speed(self.velocity)
            else:
                self.move_speed(-self.velocity)
