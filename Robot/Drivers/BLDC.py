from RPi import GPIO


class BLDC:
    
    def __init__(self, pin):
        self.speed = None
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(4)
    
    def move(self, speed):
        self.speed = ((speed - 127.0) / 128) * 100
        if speed == 127:
            self.pwm.ChangeDutyCycle(0.0)
        else:
            self.pwm.ChangeDutyCycle(4 + 0.075 * self.speed)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()

