import time

from RPi import GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

pin1 = int(15)
pin2 = int(16)
pin3 = int(18)
pin4 = int(22)

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)

while True:
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.HIGH)
    GPIO.output(pin3, GPIO.HIGH)
    GPIO.output(pin4, GPIO.HIGH)
    # time.sleep(2)
    # GPIO.output(pin1, GPIO.LOW)
    # GPIO.output(pin2, GPIO.LOW)
    # GPIO.output(pin3, GPIO.LOW)
    # GPIO.output(pin4, GPIO.LOW)
    # time.sleep(2)
