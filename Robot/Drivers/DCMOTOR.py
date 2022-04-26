import RPi.GPIO as GPIO
import time


class DCMOTOR:

    def __init__(self, first_pin, second_pin):
        self.direction = None
        self.PIN_A = first_pin
        self.PIN_B = second_pin
        GPIO.setup(self.PIN_A, GPIO.OUT)
        GPIO.setup(self.PIN_B, GPIO.OUT)

    def move(self, direction):
        self.direction = direction
        if self.direction == 127:
            GPIO.output(self.PIN_A, GPIO.LOW)
            GPIO.output(self.PIN_B, GPIO.LOW)
        elif self.direction > 127:
            GPIO.output(self.PIN_A, GPIO.HIGH)
            GPIO.output(self.PIN_B, GPIO.LOW)
        else:
            GPIO.output(self.PIN_A, GPIO.LOW)
            GPIO.output(self.PIN_B, GPIO.HIGH)