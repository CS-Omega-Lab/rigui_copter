import time
from threading import Thread

import Robot.AutoCameraStreamer as ACS

ACS.main_thread()
for i in range(0,3):
    print('ass2')
    time.sleep(1)
ACS.started = False
time.sleep(3)
ACS.main_thread()
for i in range(0,3):
    print('ass3')
    time.sleep(1)