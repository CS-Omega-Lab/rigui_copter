import time
import os

from Robot.Drivers.I2C import I2CConnector as I2C
from Robot.RobotDataManager import DataProvider as DP

os.system('clear')

dp = DP().instance()

dp.lg('ROBOT', 0, 'Запуск системы: успешно.')

i2c = I2C(dp).start()


def check_hardware():
    ret_1 = dp.check()
    ret_2 = i2c.check()
    dp.lg('ROBOT', 0, "Video system: " + str(ret_1))
    dp.lg('ROBOT', 0, "I2C device: "+str(ret_2))
    return True


dp.lg('ROBOT', 0, 'Проверяю устройства...')

if check_hardware():
    dp.lg('ROBOT', 0, 'Устройства: ОК...')
else:
    dp.lg('ROBOT', 1, 'Устройства: Ошибка, инфо выше.')

dp.lg('ROBOT', 0, 'Запускаю коннекторы...')

dp.start(i2c)

dp.lg('ROBOT', 0, 'Готов.')

while True:
    time.sleep(10)
