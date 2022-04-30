import time
import os
import configparser

from Robot.RobotDataManager import DataManager as DM
from Robot.ManualCameraStreamer import ManualCameraStreamer as MCS

config = configparser.ConfigParser()
config.read("assets/explora.cfg")

os.system('clear')
print('Запускаюсь...')

dp = DM(config).start()
mcs = MCS(dp).start()

dp.lg('ROBOT', 0, 'Робот готов.')

while True:
    time.sleep(10)
