import time
from threading import Thread
import os.path

import cv2

from Robot.RobotNetworkClient import NetworkClient as NC
from Robot.CamHandler import MjpegServer as MJS
from Robot.Drivers.GPIO import GPIOConnector as GP

from rich.console import Console


class DataProvider:
    def __init__(self):
        self.cls = Console()
        self.i2c = None
        self.nc = NC()
        self.mjs = MJS(ip='192.168.31.200', port=5045)
        self.gp = GP().start()
        self.image = cv2.imread("test.jpg")

        self.cap_0_avail = False
        #self.cap_1_avail = False
        #self.cap_2_avail = False

        self.cap_0 = None
        #self.cap_1 = None
        #self.cap_2 = None



        # МЕНЯТЬ ТУТ
        self.cam_id_0 = 0
        # self.cam_id_1 = 2
        # self.cam_id_2 = 6

        #self.prev_cam_id = self.cam_id_0
        self.thread = Thread(target=self.operate, daemon=True, args=())

    def instance(self):
        return self

    def check(self):
        if os.path.exists('/dev/video'+str(self.cam_id_0)):
            self.cap_0 = cv2.VideoCapture(self.cam_id_0, cv2.CAP_V4L2)
            self.cap_0_avail = True
            self.lg('ROBOT', 0, 'Камера с ID='+str(self.cam_id_0)+' готова.')
        else:
            self.lg('ROBOT', 1, 'Камера с ID='+str(self.cam_id_0)+' недоступна.')

        # if os.path.exists('/dev/video'+str(self.cam_id_1)):
        #     self.cap_1 = cv2.VideoCapture(self.cam_id_1, cv2.CAP_V4L2)
        #     self.cap_1_avail = True
        #     self.lg('ROBOT', 0, 'Камера с ID='+str(self.cam_id_1)+' готова.')
        # else:
        #     self.lg('ROBOT', 1, 'Камера с ID='+str(self.cam_id_1)+' недоступна.')

        # if os.path.exists('/dev/video'+str(self.cam_id_2)):
        #     self.cap_2 = cv2.VideoCapture(self.cam_id_2, cv2.CAP_V4L2)
        #     self.cap_2_avail = True
        #     self.lg('ROBOT', 0, 'Камера с ID='+str(self.cam_id_2)+' готова.')
        # else:
        #     self.lg('ROBOT', 1, 'Камера с ID='+str(self.cam_id_2)+' недоступна.')

        return True

    def start(self, i2c):
        self.i2c = i2c
        self.nc.start()
        self.thread.start()
        return self

    def operate(self):
        while True:
            time.sleep(0.01)
            cmd = self.nc.receive()
            if cmd[12]:
                self.lg('ROBOT', 2, 'ПРИНЯТА КОМАНДА ПЕРЕЗАГРУЗКИ АРДУИН.')
                self.gp.send((cmd[10], cmd[11], cmd[12]))
                time.sleep(2)
                continue
            if self.cap_0_avail:
                ret, frame = self.cap_0.read()
            else:
                frame = self.image
            # if cmd[9] == 0 and self.cap_0_avail:
            #     ret, frame = self.cap_0.read()
            #     if self.prev_cam_id != 0:
            #         self.prev_cam_id = 0
            #         time.sleep(2)
            #         ret, frame = self.cap_0.read()
            # elif cmd[9] == 1 and self.cap_1_avail:
            #     ret, frame = self.cap_1.read()
            #     if self.prev_cam_id != 1:
            #         self.prev_cam_id = 1
            #         time.sleep(2)
            #         ret, frame = self.cap_1.read()
            # elif cmd[9] == 2 and self.cap_2_avail:
            #     ret, frame = self.cap_2.read()
            #     if self.prev_cam_id != 2:
            #         self.prev_cam_id = 2
            #         time.sleep(2)
            #         ret, frame = self.cap_2.read()
            # else:
            #     ret, frame = (True, self.image)

            self.mjs.send_img(frame)
            self.i2c.send(cmd)
            self.gp.send((cmd[10], cmd[11], cmd[12]))

    def lg(self, src, typ, message):
        if typ == 0:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][white bold]INFO[/][red bold]::[/]" + message)
        elif typ == 1:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][red bold]ERROR[/][red bold]::[/]" + message)
        else:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][yellow bold]WARN[/][red bold]::[/]" + message)
