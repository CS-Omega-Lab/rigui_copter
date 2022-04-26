import time
import os

from Robot.RobotDataManager import DataProvider as DP
from Robot.ManualCameraStreamer import ManualCameraStreamer as MCS

os.system('clear')

dp = DP().start()
mcs = MCS().start()

dp.lg('ROBOT', 0, 'Робот готов.')

while True:
    time.sleep(10)
