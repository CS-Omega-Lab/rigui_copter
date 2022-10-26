import time
from threading import Thread

import keyboard

# Driving:
# wasd, ikol гусли и плавники
# 123456 манипулятор
# 789 камера
# left, right скорость
import py_win_keyboard_layout
import win32api
import win32con


class KeyManager:
    def __init__(self, hdm):

        # Включаем английскую раскладку и NumLock
        py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)
        if self.is_num_lock_on() != 1:
            keyboard.press_and_release('num lock')

        self.hdm = hdm

        # Параметры моторов и осей, 127 - среднее положение
        self.motor_params = (127, 127)
        self.fins_params = (127, 127)
        self.cam_params = (127, 127)
        self.axis_params = (127, 127, 127)

        self.max_speed = 127

        self.turn_k = 80

        self.w = False
        self.a = False
        self.s = False
        self.d = False
        self.ax_switch = False

        self.thread = Thread(target=self.update, daemon=True, args=())

    def get_vals(self):
        return [
            self.motor_params,
            self.fins_params,
            self.axis_params,
            self.cam_params
        ]

    def start(self):
        try:
            self.thread.start()
        except Exception as e:
            self.hdm.lgm.dlg('HOST', '1', 'Ошибка запуска KeyManager: '+str(e))
            self.hdm.set_boot_lock()
        self.hdm.lgm.dlg('HOST', 3, 'Запуск KeyManager: успешно.')
        self.hdm.lg('HOST', 0, 'Запуск KeyManager: успешно.')
        return self

    @staticmethod
    def is_num_lock_on():
        return win32api.GetKeyState(win32con.VK_NUMLOCK)

    def detect_key(self, e):
        if e.event_type == 'down' and e.name == '8':
            self.ax_switch = True
        if e.event_type == 'up' and e.name == '8':
            self.ax_switch = False

        if self.ax_switch:
            if e.event_type == 'down' and e.name == '9':
                self.cam_params = [self.cam_params[0], 255]
            if e.event_type == 'up' and e.name == '9':
                self.cam_params = [self.cam_params[0], 127]
            if e.event_type == 'down' and e.name == '7':
                self.cam_params = [self.cam_params[0], 0]
            if e.event_type == 'up' and e.name == '7':
                self.cam_params = [self.cam_params[0], 127]
        else:
            if e.event_type == 'down' and e.name == '9':
                self.cam_params = [255, self.cam_params[1]]
            if e.event_type == 'up' and e.name == '9':
                self.cam_params = [127, self.cam_params[1]]
            if e.event_type == 'down' and e.name == '7':
                self.cam_params = [0, self.cam_params[1]]
            if e.event_type == 'up' and e.name == '7':
                self.cam_params = [127, self.cam_params[1]]

        if e.event_type == 'down' and e.name == 'l':
            self.fins_params = [self.fins_params[0], 255]
        if e.event_type == 'up' and e.name == 'l':
            self.fins_params = [self.fins_params[0], 127]
        if e.event_type == 'down' and e.name == 'o':
            self.fins_params = [self.fins_params[0], 0]
        if e.event_type == 'up' and e.name == 'o':
            self.fins_params = [self.fins_params[0], 127]

        if e.event_type == 'down' and e.name == 'k':
            self.fins_params = [0, self.fins_params[1]]
        if e.event_type == 'up' and e.name == 'k':
            self.fins_params = [127, self.fins_params[1]]
        if e.event_type == 'down' and e.name == 'i':
            self.fins_params = [255, self.fins_params[1]]
        if e.event_type == 'up' and e.name == 'i':
            self.fins_params = [127, self.fins_params[1]]

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

        if e.event_type == 'down' and e.name == '5':
            self.axis_params = [255, self.axis_params[1], self.axis_params[2]]
        if e.event_type == 'up' and e.name == '5':
            self.axis_params = [127, self.axis_params[1], self.axis_params[2]]
        if e.event_type == 'down' and e.name == '2':
            self.axis_params = [0, self.axis_params[1], self.axis_params[2]]
        if e.event_type == 'up' and e.name == '2':
            self.axis_params = [127, self.axis_params[1], self.axis_params[2]]

        if e.event_type == 'down' and e.name == '6':
            self.axis_params = [self.axis_params[0], 255, self.axis_params[2]]
        if e.event_type == 'up' and e.name == '6':
            self.axis_params = [self.axis_params[0], 127, self.axis_params[2]]
        if e.event_type == 'down' and e.name == '4':
            self.axis_params = [self.axis_params[0], 0, self.axis_params[2]]
        if e.event_type == 'up' and e.name == '4':
            self.axis_params = [self.axis_params[0], 127, self.axis_params[2]]

        if e.event_type == 'down' and e.name == '3':
            self.axis_params = [self.axis_params[0], self.axis_params[1], 255]
        if e.event_type == 'up' and e.name == '3':
            self.axis_params = [self.axis_params[0], self.axis_params[1], 127]
        if e.event_type == 'down' and e.name == '1':
            self.axis_params = [self.axis_params[0], self.axis_params[1], 0]
        if e.event_type == 'up' and e.name == '1':
            self.axis_params = [self.axis_params[0], self.axis_params[1], 127]

    def m_forward(self):
        return 127 + self.max_speed

    def m_backward(self):
        return 127 - self.max_speed

    def dec_speed(self):
        if self.max_speed - 5 >= 27:
            self.max_speed -= 5

    def inc_speed(self):
        if self.max_speed + 5 <= 127:
            self.max_speed += 5

    def update(self):
        keyboard.hook_key('w', self.detect_key)
        keyboard.hook_key('a', self.detect_key)
        keyboard.hook_key('s', self.detect_key)
        keyboard.hook_key('d', self.detect_key)

        keyboard.hook_key('i', self.detect_key)
        keyboard.hook_key('k', self.detect_key)
        keyboard.hook_key('o', self.detect_key)
        keyboard.hook_key('l', self.detect_key)

        keyboard.hook_key('left', self.detect_key)
        keyboard.hook_key('right', self.detect_key)

        keyboard.hook_key('1', self.detect_key)
        keyboard.hook_key('2', self.detect_key)
        keyboard.hook_key('3', self.detect_key)
        keyboard.hook_key('4', self.detect_key)
        keyboard.hook_key('5', self.detect_key)
        keyboard.hook_key('6', self.detect_key)
        keyboard.hook_key('7', self.detect_key)
        keyboard.hook_key('8', self.detect_key)
        keyboard.hook_key('9', self.detect_key)
        keyboard.wait()
