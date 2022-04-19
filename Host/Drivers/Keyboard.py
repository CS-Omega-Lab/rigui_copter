import time
from threading import Thread

import keyboard


class Keyboard:
    def __init__(self, srs, config):
        self.srs = srs

        # True - Drive, False - Manipulate
        self.mode = True

        # 127 is 0
        self.motor_params = (127, 127)
        self.fins_params = (127, 127)
        self.max_speed = 127
        self.speed_params = (37, 127)
        self.turn_k = 20
        self.w = False
        self.a = False
        self.s = False
        self.d = False

        self.axis_params = 127
        self.current_axis = 0

        self.thread = Thread(target=self.update, daemon=True, args=())

    def get_state(self):
        return [
            self.mode,
            self.motor_params,
            self.fins_params,
            self.max_speed,
            self.current_axis,
            self.axis_params
        ]

    def start(self):
        self.thread.start()
        self.srs.lg('HOST', 0, 'Запуск перехвата клавиатуры: успешно.')
        return self

    def detect_key(self, e):

        if e.event_type == 'up' and e.name == 'm':
            self.mode = not self.mode
            return

        if e.event_type == 'down' and e.name == '8':
            self.fins_params = [self.fins_params[0], 255]
        if e.event_type == 'up' and e.name == '8':
            self.fins_params = [self.fins_params[0], 127]
        if e.event_type == 'down' and e.name == '2':
            self.fins_params = [self.fins_params[0], 0]
        if e.event_type == 'up' and e.name == '2':
            self.fins_params = [self.fins_params[0], 127]

        if e.event_type == 'down' and e.name == '4':
            self.fins_params = [0, self.fins_params[1]]
        if e.event_type == 'up' and e.name == '4':
            self.fins_params = [127, self.fins_params[1]]
        if e.event_type == 'down' and e.name == '6':
            self.fins_params = [255, self.fins_params[1]]
        if e.event_type == 'up' and e.name == '6':
            self.fins_params = [127, self.fins_params[1]]

        if self.mode:
            if e.event_type == 'down' and e.name == 'w':
                self.w = True
            if e.event_type == 'up' and e.name == 'w':
                self.w = False
            if e.event_type == 'down' and e.name == 'a':
                self.a = True
            if e.event_type == 'up' and e.name == 'a':
                self.a = False
            if e.event_type == 'down' and e.name == 's':
                self.s = True
            if e.event_type == 'up' and e.name == 's':
                self.s = False
            if e.event_type == 'down' and e.name == 'd':
                self.d = True
            if e.event_type == 'up' and e.name == 'd':
                self.d = False

            if self.w and (not self.a) and (not self.s) and (not self.d):
                self.motor_params = (self.m_forward(), self.m_forward())
            if self.w and self.a and (not self.s) and (not self.d):
                self.motor_params = (self.m_forward() - self.turn_k, self.m_forward())
            if self.w and (not self.a) and (not self.s) and self.d:
                self.motor_params = (self.m_forward(), self.m_forward() - self.turn_k)

            if self.a and (not self.w) and (not self.s) and (not self.d):
                self.motor_params = (self.m_backward(), self.m_forward())
            if self.d and (not self.w) and (not self.s) and (not self.a):
                self.motor_params = (self.m_forward(), self.m_backward())

            if self.s and (not self.a) and (not self.w) and (not self.d):
                self.motor_params = (self.m_backward(), self.m_backward())
            if self.s and self.a and (not self.w) and (not self.d):
                self.motor_params = (self.m_backward() + self.turn_k, self.m_backward())
            if self.s and (not self.a) and (not self.w) and self.d:
                self.motor_params = (self.m_backward(), self.m_backward() + self.turn_k)

            if (not self.w) and (not self.a) and (not self.s) and (not self.d):
                self.motor_params = (127, 127)

            # ВНИМАНИЕ: ЛЮТЫЙ КОСТЫЛЬ. ПРИ ИСПОЛЬЗОВАНИИ СТРЕЛОЧЕК ОНИ ПОЧЕМУ-ТО ВЫЗЫВАЮТ ИВЕНТ 2 РАЗА
            # СООТВЕТСТВЕННО УМЕНЬШАЕМ НА ПОЛОВИНУ ЗНАЧЕНИЯ
            if e.event_type == 'up' and e.name == 'left':
                self.dec_speed()
            if e.event_type == 'up' and e.name == 'right':
                self.inc_speed()
        else:
            if e.event_type == 'up' and e.name == 'a':
                self.prev_link()
            if e.event_type == 'up' and e.name == 'd':
                self.next_link()

            if e.event_type == 'down' and e.name == 'w':
                self.axis_params = 255
            if e.event_type == 'up' and e.name == 'w':
                self.axis_params = 127
            if e.event_type == 'down' and e.name == 's':
                self.axis_params = 0
            if e.event_type == 'up' and e.name == 's':
                self.axis_params = 127

    def m_forward(self):
        return 127 + self.max_speed

    def m_backward(self):
        return 127 - self.max_speed

    def dec_speed(self):
        if self.max_speed - 5 >= self.speed_params[0]:
            self.max_speed -= 5

    def inc_speed(self):
        if self.max_speed + 5 <= self.speed_params[1]:
            self.max_speed += 5

    def prev_link(self):
        if self.current_axis == 0:
            self.current_axis = 3
        else:
            self.current_axis -= 1

    def next_link(self):
        if self.current_axis == 3:
            self.current_axis = 0
        else:
            self.current_axis += 1

    def update(self):
        keyboard.hook_key('w', self.detect_key)
        keyboard.hook_key('a', self.detect_key)
        keyboard.hook_key('s', self.detect_key)
        keyboard.hook_key('d', self.detect_key)

        keyboard.hook_key('left', self.detect_key)
        keyboard.hook_key('right', self.detect_key)

        keyboard.hook_key('m', self.detect_key)

        keyboard.hook_key('8', self.detect_key)
        keyboard.hook_key('4', self.detect_key)
        keyboard.hook_key('2', self.detect_key)
        keyboard.hook_key('6', self.detect_key)
        keyboard.wait()
        # time.sleep(0.001)
