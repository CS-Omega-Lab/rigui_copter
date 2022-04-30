# noinspection PyUnresolvedReferences
from RPi import GPIO


class BLDC:
    def __init__(self, pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.pin = int(pin)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0.0)
    
    def move(self, speed):
        c_speed = ((speed - 127.0) / 18.2)
        if speed == 127:
            self.pwm.ChangeDutyCycle(0.0)
        else:
            self.pwm.ChangeDutyCycle(4 + c_speed)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()

