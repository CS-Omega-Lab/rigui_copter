import time
from threading import Thread
import RPi.GPIO as GPIO


def inc_angle(a):
    if a + 10 < 175:
        return a + 10
    else:
        return a


def dec_angle(a):
    if a - 10 > 0:
        return a - 10
    else:
        return a


def calc_angle(angle):
    if angle > 175:
        an = 175
    else:
        an = angle
    return an / 18 + 3


class GPIOConnector:
    def __init__(self):
        self.cmd = [127, 127, 0]
        self.angle_1 = 90
        self.angle_2 = 90
        self.thread = Thread(target=self.write, daemon=True, args=())

    def start(self):
        self.thread.start()
        return self

    def send(self, cmd):
        self.cmd = cmd

    def write(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)
        pwm_1 = GPIO.PWM(11, 50)
        pwm_2 = GPIO.PWM(13, 50)
        pwm_1.start(0)
        pwm_2.start(0)
        pwm_1.ChangeDutyCycle(calc_angle(90))
        pwm_2.ChangeDutyCycle(calc_angle(90))
        time.sleep(0.8)
        while True:
            time.sleep(0.05)
            try:
                if self.cmd[2]:
                    GPIO.output(15, GPIO.HIGH)
                    continue
                else:
                    GPIO.output(15, GPIO.LOW)

                if self.cmd[0] > 127:
                    self.angle_1 = inc_angle(self.angle_1)
                    pwm_1.ChangeDutyCycle(calc_angle(self.angle_1))
                    time.sleep(0.1)
                elif self.cmd[0] < 127:
                    self.angle_1 = dec_angle(self.angle_1)
                    pwm_1.ChangeDutyCycle(calc_angle(self.angle_1))
                    time.sleep(0.1)
                else:
                    pwm_1.ChangeDutyCycle(0)

                if self.cmd[1] > 127:
                    self.angle_2 = inc_angle(self.angle_2)
                    pwm_2.ChangeDutyCycle(calc_angle(self.angle_2))
                    time.sleep(0.1)
                elif self.cmd[1] < 127:
                    self.angle_2 = dec_angle(self.angle_2)
                    pwm_2.ChangeDutyCycle(calc_angle(self.angle_2))
                    time.sleep(0.1)
                else:
                    pwm_2.ChangeDutyCycle(0)
            except KeyboardInterrupt:
                pwm_1.stop()
                pwm_2.stop()
                GPIO.cleanup()
