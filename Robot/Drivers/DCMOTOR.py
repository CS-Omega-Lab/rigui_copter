# noinspection PyUnresolvedReferences
from RPi import GPIO


class DCMOTOR:
    def __init__(self, first_pin, second_pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.PIN_A = int(first_pin)
        self.PIN_B = int(second_pin)
        GPIO.setup(self.PIN_A, GPIO.OUT)
        GPIO.setup(self.PIN_B, GPIO.OUT)

    def move(self, direction):
        if direction == 127:
            GPIO.output(self.PIN_A, GPIO.LOW)
            GPIO.output(self.PIN_B, GPIO.LOW)
        elif direction > 127:
            GPIO.output(self.PIN_A, GPIO.HIGH)
            GPIO.output(self.PIN_B, GPIO.LOW)
        else:
            GPIO.output(self.PIN_A, GPIO.LOW)
            GPIO.output(self.PIN_B, GPIO.HIGH)

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()
