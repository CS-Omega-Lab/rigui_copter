import time
from threading import Thread
import cv2

import sys


class CamViewHandler:
    def __init__(self, srs, ns):
        self.srs = srs
        self.ns = ns
        self.active = False
        self.cam_id = 0
        self.close_win = False
        self.thread = Thread(target=self.display, daemon=True, args=())
        self.img = cv2.imread("test.jpg")

    def start(self):
        self.thread.start()
        return self

    def update_info(self, mode):
        if self.cam_id != mode[6]:
            self.close_win = True
        self.cam_id = mode[6]
        if mode[0]:
            self.active = True
        else:
            self.active = False

    def display(self):
        image = self.img
        while True:
            time.sleep(0.01)
            image = self.ns.get_image()
            if self.close_win:
                cv2.destroyAllWindows()
                self.close_win = False
            if self.active:
                cv2.imshow('Stream '+str(self.cam_id), image)
                cv2.waitKey(1)
            else:
                cv2.destroyAllWindows()
