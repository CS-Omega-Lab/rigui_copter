#!/usr/bin/python3.9
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import time
import configparser

from Platform.DataManager import DataManager
from Common.LogManager import LogManager
from Common.AddressManager import AddressManager

lgm = LogManager()
config = configparser.ConfigParser()
config.read("Assets/explora.cfg")

lgm.dlg("PLTF", 3, "Запускаюсь...")

am = AddressManager(lgm, config)
am.wait_for_network()

data_manager = DataManager(config, lgm).start()

lgm.dlg('PLTF', 3, 'Робот готов.')

while True:
    time.sleep(0.1)
