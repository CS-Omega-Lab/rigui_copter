from inputs import get_gamepad
import threading

from Common.ConstStorage import ConstStorage as CS


class GPManager(object):
    MAX_TRIG_VAL = 2.01
    MAX_JOY_VAL = 16.01

    def __init__(self, hdm):

        self.hdm = hdm
        self.lj_y = 0
        self.lj_x = 0
        self.rj_y = 0
        self.rj_x = 0
        self.lt = 0
        self.rt = 0
        self.lb = 0
        self.rb = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.lp_y = 0
        self.lp_x = 0

        self.CopterX = CS.MID_VAL
        self.CopterY = CS.MID_VAL
        self.CopterZ = CS.MID_VAL
        self.CopterYW = CS.MID_VAL

        self.CopterArmed = 0
        self.CopterMode = 0

        self.rb_last = 0
        self.lb_last = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True

    def start(self):
        try:
            get_gamepad()
            self._monitor_thread.start()
            self.hdm.lgm.dlg('HOST', 3, 'Запуск GPManager: успешно.')
            self.hdm.lg('HOST', 0, 'Запуск GPManager: успешно.')
        except Exception as e:
            self.hdm.lgm.dlg('HOST', 1, 'Ошибка запуска GPManager: '+str(e))
            self.hdm.set_boot_lock()
        return self

    def get_vals(self):
        return [
            self.CopterX,
            self.CopterY,
            self.CopterZ,
            self.CopterYW,
            self.CopterArmed,
            self.CopterMode
        ]

    def _monitor_controller(self):
        while True:
            self.CopterX = CS.MID_VAL + self.rj_x if abs(self.rj_x) > 320 else CS.MID_VAL

            self.CopterY = CS.MID_VAL + self.rj_y if abs(self.rj_y) > 320 else CS.MID_VAL
            self.CopterZ = CS.MID_VAL + self.lj_x if abs(self.lj_x) > 320 else CS.MID_VAL

            self.CopterYW = CS.MID_VAL + self.lj_y if abs(self.lj_y) > 320 else CS.MID_VAL

            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.lj_y = int(event.state / GPManager.MAX_JOY_VAL)
                elif event.code == 'ABS_X':
                    self.lj_x = int(event.state / GPManager.MAX_JOY_VAL)
                elif event.code == 'ABS_RY':
                    self.rj_y = int(event.state / GPManager.MAX_JOY_VAL)
                elif event.code == 'ABS_RX':
                    self.rj_x = int(event.state / GPManager.MAX_JOY_VAL)
                elif event.code == 'ABS_Z':
                    self.lt = int(event.state / GPManager.MAX_TRIG_VAL)
                elif event.code == 'ABS_RZ':
                    self.rt = int(event.state / GPManager.MAX_TRIG_VAL)
                elif event.code == 'BTN_TL':
                    self.lb = event.state
                    if (not event.state) and self.lb_last:
                        self.CopterArmed = CS.MAX_VAL if self.CopterArmed == 0 else 0
                    self.lb_last = event.state
                elif event.code == 'BTN_TR':
                    self.rb = event.state
                    if (not event.state) and self.rb_last:
                        if self.CopterMode+CS.MID_VAL > CS.MAX_VAL:
                            self.CopterMode = 0
                        else:
                            self.CopterMode += CS.MID_VAL
                    self.rb_last = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state
                elif event.code == 'BTN_WEST':
                    self.X = 127 if event.state else 0
                elif event.code == 'BTN_EAST':
                    self.B = 127 if event.state else 0
                elif event.code == 'ABS_HAT0Y':
                    self.lp_y = event.state * 127
                elif event.code == 'ABS_HAT0X':
                    self.lp_x = event.state * 127
