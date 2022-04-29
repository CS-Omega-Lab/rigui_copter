import time
from threading import Thread

import keyboard

# Driving:
# wasd,8456 гусли и плавники
# 123 камера
# 0 смена режима ручной работы
# m смена режима на полуавтоматический
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

        # Режим управления: ручной (True) или полуавтомат (False)
        self.robot_mode = True
        # Режим передачи данных для ручного режима: езда (True) или манипулятор (False)
        self.manual_mode = True
        # Максимальная скорость
        self.max_speed = 127

        # Параметры моторов и осей, 127 - среднее положение
        self.motor_params = (127, 127)
        self.fins_params = (127, 127)
        self.cam_params = (127, 127)

        self.turn_k = 20

        self.w = False
        self.a = False
        self.s = False
        self.d = False
        self.dva = False

        self.axis_params = 127
        self.current_axis = 0

        # Параметры для полуавтомат режима
        self.current_preset = 0
        self.presets = [
            1.0,
            1.0,
            1.0,
            1.0,
            1.0
        ]
        self.active = True

        self.thread = Thread(target=self.update, daemon=True, args=())

    def get_mode(self):
        return [
            self.robot_mode,
            self.manual_mode,
            self.max_speed,
            self.current_preset,
            self.presets[self.current_preset]
        ]

    def get_vals(self):
        return [
            self.motor_params,
            self.fins_params,
            self.current_axis,
            self.axis_params,
            self.cam_params
        ]

    def start(self):
        self.thread.start()
        self.hdm.lg('HOST', 0, 'Запуск KeyManager: успешно.')
        return self

    def is_num_lock_on(self):
        return win32api.GetKeyState(win32con.VK_NUMLOCK)

    def detect_key(self, e):

        if e.event_type == 'down' and e.name == '2':
            self.dva = True
        if e.event_type == 'up' and e.name == '2':
            self.dva = False

        if self.dva:
            if e.event_type == 'down' and e.name == '3':
                self.cam_params = [self.cam_params[0], 255]
            if e.event_type == 'up' and e.name == '3':
                self.cam_params = [self.cam_params[0], 127]
            if e.event_type == 'down' and e.name == '1':
                self.cam_params = [self.cam_params[0], 0]
            if e.event_type == 'up' and e.name == '1':
                self.cam_params = [self.cam_params[0], 127]
        else:
            if e.event_type == 'down' and e.name == '3':
                self.cam_params = [255, self.cam_params[1]]
            if e.event_type == 'up' and e.name == '3':
                self.cam_params = [127, self.cam_params[1]]
            if e.event_type == 'down' and e.name == '1':
                self.cam_params = [0, self.cam_params[1]]
            if e.event_type == 'up' and e.name == '1':
                self.cam_params = [127, self.cam_params[1]]

        if not self.active:
            return

        if e.event_type == 'up' and e.name == '0':
            self.manual_mode = not self.manual_mode
            return
        if e.event_type == 'up' and e.name == 'm':
            self.robot_mode = not self.robot_mode
            if self.robot_mode:
                self.hdm.lg('HOST', 2, 'Перехожу в РУЧНОЙ РЕЖИМ')
            else:
                self.hdm.lg('HOST', 2, 'Перехожу в ПОЛУАВТОМАТИЧЕСКИЙ РЕЖИМ')
            return

        if e.event_type == 'down' and e.name == '8':
            self.fins_params = [self.fins_params[0], 255]
        if e.event_type == 'up' and e.name == '8':
            self.fins_params = [self.fins_params[0], 127]
        if e.event_type == 'down' and e.name == '5':
            self.fins_params = [self.fins_params[0], 0]
        if e.event_type == 'up' and e.name == '5':
            self.fins_params = [self.fins_params[0], 127]

        if e.event_type == 'down' and e.name == '4':
            self.fins_params = [0, self.fins_params[1]]
        if e.event_type == 'up' and e.name == '4':
            self.fins_params = [127, self.fins_params[1]]
        if e.event_type == 'down' and e.name == '6':
            self.fins_params = [255, self.fins_params[1]]
        if e.event_type == 'up' and e.name == '6':
            self.fins_params = [127, self.fins_params[1]]

        if self.robot_mode:
            if self.manual_mode:
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
        else:
            if e.event_type == 'up' and e.name == 'left':
                self.dec_speed()
            if e.event_type == 'up' and e.name == 'right':
                self.inc_speed()

            if e.event_type == 'up' and e.name == 's':
                self.dec_time()
            if e.event_type == 'up' and e.name == 'w':
                self.inc_time()

            if e.event_type == 'up' and e.name == 'a':
                self.prev_preset()
            if e.event_type == 'up' and e.name == 'd':
                self.next_preset()

            if e.event_type == 'up' and e.name == 'space':
                self.hdm.lg('HOST', 0, 'Запуск автономной программы ['+str(self.current_preset)+']...')
                self.motor_params = [self.m_forward(), self.m_forward()]
                self.active = False
                time.sleep(self.presets[self.current_preset])
                self.active = True
                self.hdm.lg('HOST', 0, 'Автономная программа [' + str(self.current_preset) + '] завершена.')

    def m_forward(self):
        return 127 + self.max_speed

    def m_backward(self):
        return 127 - self.max_speed

    def prev_preset(self):
        if self.current_preset == 0:
            self.current_preset = 4
        else:
            self.current_preset -= 1

    def next_preset(self):
        if self.current_preset == 4:
            self.current_preset = 0
        else:
            self.current_preset += 1

    def dec_time(self):
        if self.presets[self.current_preset]-0.1 >= 0:
            self.presets[self.current_preset] = round(self.presets[self.current_preset] - 0.1,1)

    def inc_time(self):
        self.presets[self.current_preset] = round(self.presets[self.current_preset] + 0.1,1)

    def dec_speed(self):
        if self.max_speed - 5 >= 27:
            self.max_speed -= 5

    def inc_speed(self):
        if self.max_speed + 5 <= 127:
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
        keyboard.hook_key('up', self.detect_key)
        keyboard.hook_key('down', self.detect_key)

        keyboard.hook_key('m', self.detect_key)
        keyboard.hook_key('space', self.detect_key)

        keyboard.hook_key('1', self.detect_key)
        keyboard.hook_key('2', self.detect_key)
        keyboard.hook_key('3', self.detect_key)
        keyboard.hook_key('4', self.detect_key)
        keyboard.hook_key('5', self.detect_key)
        keyboard.hook_key('6', self.detect_key)
        keyboard.hook_key('8', self.detect_key)
        keyboard.hook_key('0', self.detect_key)
        keyboard.wait()
        # time.sleep(0.001)
