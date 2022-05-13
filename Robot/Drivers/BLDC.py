# noinspection PyUnresolvedReferences
from RPi import GPIO


class BLDC:
    def __init__(self, pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.pin = int(pin)
        # print(pin)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(7.0)
    
    def move(self, speed):
        if speed == 127:
            self.pwm.ChangeDutyCycle(7.0)
        elif speed > 127:
            self.pwm.ChangeDutyCycle(7.0 + (speed-127) * 2.0 / 128)
        else:
            self.pwm.ChangeDutyCycle(7.0 - (127-speed) * 2.0 / 128)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()

