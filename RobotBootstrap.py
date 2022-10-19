#!/usr/bin/python3.9
import time
import os
import configparser

from Robot.RobotDataManager import DataManager

print('Жду сеть...')
for i in range(0, 12):
    print(i*10, 'сек')
    time.sleep(10)

config = configparser.ConfigParser()
config.read("assets/explora.cfg")

os.system('clear')
print('Запускаюсь...')

data_manager = DataManager(config).start()

data_manager.lg('ROBOT', 0, 'Робот готов.')

while True:
    time.sleep(10)
