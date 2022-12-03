#!/usr/bin/python3.9
import time
import os
import configparser
from netifaces import interfaces, ifaddresses, AF_INET

from Robot.RobotDataManager import DataManager
from Common.LogManager import LogManager
from Common.AddressManager import AddressManager

lgm = LogManager()
config = configparser.ConfigParser()
config.read("Assets/explora.cfg")

lgm.dlg("ROBOT", 3, "Запускаюсь...")

am = AddressManager(lgm)
am.wait_for_network(config['network']['subnet'])

data_manager = DataManager(config, lgm).start()

lgm.dlg('ROBOT', 3, 'Робот готов.')

while True:
    time.sleep(10)
