# noinspection PyUnresolvedReferences
import serial
import time
import os


class ILYUSHA:
    def __init__(self, rdm, ch_id, lgm):
        self.lgm = lgm
        self.poss = None
        self.rdm = rdm
        self.available = True
        self.flag = True
        self.ID = int(ch_id)
        self.velocity = 50
        self.stop_flag = True
        self.boot_time = 0
        self.got_ping = True
        if not os.path.exists(rdm.devices['uart-ttl_dev']):
            lgm.dlg('ROBOT', 1, 'Устройство UART-TTL на '+rdm.devices['uart-ttl_dev']+' не подключено.')
            self.rdm.update_init_data(1, 2)
            self.available = False
        else:
            self.ser = serial.Serial(rdm.devices['uart-ttl_dev'], 115200)
            lgm.dlg('ROBOT', 0, 'Устройство UART-TTL на ' + rdm.devices['uart-ttl_dev'] + ' подключено.')
            self.rdm.update_init_data(1, 1)
            lgm.dlg('ROBOT', 0, 'Пингую устройство UART-TTL на ' + rdm.devices['uart-ttl_dev'] + ', ID=' + ch_id + '...')
            while self.flag:
                self.ping()
                time.sleep(0.1)
                self.boot_time += 1
                if self.boot_time >= 60:
                    lgm.dlg('ROBOT', 1,
                            'Устройство UART-TTL на ' + rdm.devices['uart-ttl_dev'] + ', ID=' + ch_id + ' не ответило.')
                    self.got_ping = False
                    self.available = False
                    break
            if self.got_ping:
                lgm.dlg('ROBOT', 0, 'Устройство UART-TTL на ' + rdm.devices['uart-ttl_dev'] + ', ID=' + ch_id + ' готово.')

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
            while self.ser.inWaiting():
                data.append(self.ser.read())
            datum = None
            try:
                datum = [int.from_bytes(data[5], byteorder='big'), int.from_bytes(data[6], byteorder='big')]
            except Exception as e:
                self.lgm.dlg('ROBOT', 1, 'Устройство UART-TTL не прислало данные.')
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
            while self.ser.inWaiting():
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
            while self.ser.inWaiting():
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
            while self.ser.inWaiting():
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
            while self.ser.inWaiting():
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
