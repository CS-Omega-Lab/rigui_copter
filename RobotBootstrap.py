import time
import os
import configparser

from Robot.RobotDataManager import DataManager

config = configparser.ConfigParser()
config.read("assets/explora.cfg")

os.system('clear')
print('Запускаюсь...')

data_manager = DataManager(config).start()

data_manager.lg('ROBOT', 0, 'Робот готов.')

while True:
    time.sleep(10)
