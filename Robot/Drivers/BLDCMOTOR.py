# noinspection PyUnresolvedReferences
from RPi import GPIO
import time


class BLDCMOTOR:
    def __init__(self, pin, config, lgm):
        self.config = config
        self.lgm = lgm
        self.middle_point = float(self.config['devices-config']['bldc_middle_point'])
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.pin = int(pin)
        self.last_state = True
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(self.middle_point)

    def move(self, speed):
        if speed == 127:
            self.pwm.ChangeDutyCycle(self.middle_point)
        elif speed > 127:
            self.pwm.ChangeDutyCycle(self.middle_point + (speed - 127) * 2.0 / 128)
            self.last_state = True
        else:
            if self.last_state:
                self.pwm.ChangeDutyCycle(self.middle_point - (127 - speed) * 2.0 / 128)
                time.sleep(0.2)
                self.pwm.ChangeDutyCycle(self.middle_point)
                time.sleep(0.2)
            self.pwm.ChangeDutyCycle(self.middle_point - (127 - speed) * 2.0 / 128)
            self.last_state = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()
