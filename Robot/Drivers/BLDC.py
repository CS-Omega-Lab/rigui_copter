# noinspection PyUnresolvedReferences
from RPi import GPIO


class BLDC:
    def __init__(self, pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.pin = int(pin)
        self.last_state = None
        # print(pin)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(7.5)

    def move(self, speed):
        if speed == 127:
            self.pwm.ChangeDutyCycle(7.5)
        elif speed > 127:
            self.pwm.ChangeDutyCycle(7.5 + (speed - 127) * 2.0 / 128)
            self.last_state = True
        else:
            if self.last_state:
                self.pwm.ChangeDutyCycle(7.5 - (127 - speed) * 2.0 / 128)
                time.sleep(0.1)
                self.pwm.ChangeDutyCycle(7.5)
                time.sleep(0.1)
            self.pwm.ChangeDutyCycle(7.5 - (127 - speed) * 2.0 / 128)
            self.last_state = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()
