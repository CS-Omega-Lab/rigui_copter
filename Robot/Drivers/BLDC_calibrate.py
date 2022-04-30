# noinspection PyUnresolvedReferences
from RPi import GPIO
import configparser

config = configparser.ConfigParser()
config.read("assets/explora.cfg")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

l_pin = int(config['devices']['left_motor'])
r_pin = int(config['devices']['right_motor'])

GPIO.setup(l_pin, GPIO.OUT)
GPIO.setup(r_pin, GPIO.OUT)
self.l_pwm = GPIO.PWM(l_pin, 50)
self.r_pwm = GPIO.PWM(r_pin, 50)
l_pwm.start(0.0)
r_pwm.start(0.0)

print('Отключи батарею и нажми ENTER')
inp = raw_input()
if inp == '':
    l_pwm.ChangeDutyCycle(11.0)
    r_pwm.ChangeDutyCycle(11.0)
    print('Калибровка высокого уровня...')
    print('Подключи батарею, подожди писк и нажми ENTER')
    inp = raw_input()
    if inp == '':
        print('Калибровка низкого уровня...')
        l_pwm.ChangeDutyCycle(4.0)
        r_pwm.ChangeDutyCycle(4.0)
        time.sleep(3)
        print('Калибровка нулевого уровня...')
        l_pwm.ChangeDutyCycle(0.0)
        r_pwm.ChangeDutyCycle(0.0)
        time.sleep(3)
        print('Запуск ESC...')
        l_pwm.ChangeDutyCycle(4.0)
        r_pwm.ChangeDutyCycle(4.0)
        time.sleep(3)
        inp = input('Проверить работу? (y/n)')
        if inp == 'y':
            l_pwm.ChangeDutyCycle(6.0)
            r_pwm.ChangeDutyCycle(6.0)
            time.sleep(3)
        print('Завершение...')

GPIO.cleanup()
