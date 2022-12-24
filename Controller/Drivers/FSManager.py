import ctypes
from threading import Thread

from Common.ConstStorage import ConstStorage as CS


class FSManager:

    def __init__(self, hdm):
        self.hdm = hdm
        self.wab = WinApiBinding(hdm)
        self.ret, self.caps, self.st_info = False, None, None

        self.vals = [
            CS.MID_VAL,  # Roll
            CS.MID_VAL,  # Pitch
            CS.MID_VAL,  # Yaw
            CS.MIN_VAL,  # Throttle
            CS.MIN_VAL,  # T1
            CS.MIN_VAL,  # T2
            CS.MIN_VAL,  # T3
            CS.MIN_VAL   # T4
        ]

        self.thread = Thread(target=self.update, daemon=True, args=())

    def start(self):
        try:
            self.hdm.lgm.dlg('CNTR', 3, 'Ожидаю отклик аппаратуры...')
            self.ret, self.caps = self.wab.joyGetDevCaps(0)
            if self.ret:
                self.ret, self.st_info = self.wab.joyGetPosEx(0)
                self.thread.start()
                self.hdm.lgm.dlg('CNTR', 3, 'Запуск FSManager: успешно.')
                self.hdm.lg('CNTR', 0, 'Запуск FSManager: успешно.')
            else:
                self.hdm.lgm.dlg('CNTR', 1, 'Ошибка запуска FSManager: аппаратура не подключена или не отвечает.')
                self.hdm.set_boot_lock()
        except Exception as e:
            self.hdm.lgm.dlg('CNTR', 1, 'Ошибка запуска FSManager: ' + str(e))
            self.hdm.set_boot_lock()
        return self

    def get_vals(self):
        return self.vals

    def update(self):
        while True:
            ret, info = self.wab.joyGetPosEx(0)
            if ret:
                buttons = [(1 << i) & info.dwButtons != 0 for i in range(self.caps.wNumButtons)]
                axis_xyz = [info.dwXpos - self.st_info.dwXpos, info.dwYpos - self.st_info.dwYpos,
                            info.dwZpos - self.st_info.dwZpos]
                axis_ruv = [info.dwRpos - self.st_info.dwRpos, info.dwUpos - self.st_info.dwUpos,
                            info.dwVpos - self.st_info.dwVpos]
                self.vals = [
                    int(CS.MID_VAL + axis_xyz[0] / CS.MAX_JOY_VAL),
                    int(CS.MID_VAL + axis_xyz[1] / CS.MAX_JOY_VAL),
                    int(CS.MID_VAL + axis_ruv[2] / CS.MAX_JOY_VAL),
                    int(CS.MID_VAL + axis_xyz[2] / CS.MAX_JOY_VAL),
                    CS.MAX_VAL if buttons[7] > CS.MIN_VAL else CS.MIN_VAL,
                    CS.MAX_VAL if buttons[3] > CS.MIN_VAL else CS.MIN_VAL,
                    CS.MAX_VAL if axis_ruv[1] > CS.MIN_VAL else CS.MID_VAL if axis_ruv[1] == CS.MIN_VAL else CS.MIN_VAL,
                    CS.MAX_VAL if axis_ruv[0] > CS.MIN_VAL else CS.MIN_VAL,
                ]


class WinApiBinding:
    def __init__(self, hdm):
        try:
            winmm_dll = ctypes.WinDLL('winmm.dll')
            joy_get_num_devs_proto = ctypes.WINFUNCTYPE(ctypes.c_uint)
            self.joy_get_num_devs_func = joy_get_num_devs_proto(("joyGetNumDevs", winmm_dll))

            joy_get_dev_caps_proto = ctypes.WINFUNCTYPE(ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint)
            joy_get_dev_caps_param = (1, "uJoyID", 0), (1, "pjc", None), (1, "cbjc", 0)
            self.joy_get_dev_caps_func = joy_get_dev_caps_proto(("joyGetDevCapsW", winmm_dll), joy_get_dev_caps_param)

            joy_get_pos_ex_proto = ctypes.WINFUNCTYPE(ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p)
            joy_get_pos_ex_param = (1, "uJoyID", 0), (1, "pji", None)
            self.joy_get_pos_ex_func = joy_get_pos_ex_proto(("joyGetPosEx", winmm_dll), joy_get_pos_ex_param)
        except Exception as e:
            hdm.lgm.dlg('CNTR', 1, 'Ошибка запуска FSManager: ' + str(e))

    def joyGetNumDevs(self):
        try:
            num = self.joy_get_num_devs_func()
        except:
            num = 0
        return num

    def joyGetDevCaps(self, u_joy_id):
        try:
            buffer = (ctypes.c_ubyte * JOYCAPS.SIZE_W)()
            p1 = ctypes.c_uint(u_joy_id)
            p2 = ctypes.cast(buffer, ctypes.c_void_p)
            p3 = ctypes.c_uint(JOYCAPS.SIZE_W)
            ret_val = self.joy_get_dev_caps_func(p1, p2, p3)
            ret = (False, None) if ret_val != JOYCAPS.JOYERR_NOERROR else (True, JOYCAPS(buffer))
        except:
            ret = False, None
        return ret

    def joyGetPosEx(self, u_joy_id):
        try:
            buffer = (ctypes.c_uint32 * (JOYINFOEX.SIZE // 4))()
            buffer[0] = JOYINFOEX.SIZE
            buffer[1] = JOYCAPS.JOY_RETURNALL
            p1 = ctypes.c_uint(u_joy_id)
            p2 = ctypes.cast(buffer, ctypes.c_void_p)
            ret_val = self.joy_get_pos_ex_func(p1, p2)
            ret = (False, None) if ret_val != JOYCAPS.JOYERR_NOERROR else (True, JOYINFOEX(buffer))
        except:
            ret = False, None
        return ret


class JOYCAPS:
    SIZE_W = 728
    OFFSET_V = 4 + 32 * 2

    JOYERR_NOERROR = 0
    JOY_RETURNX = 0x00000001
    JOY_RETURNY = 0x00000002
    JOY_RETURNZ = 0x00000004
    JOY_RETURNR = 0x00000008
    JOY_RETURNU = 0x00000010
    JOY_RETURNV = 0x00000020
    JOY_RETURNPOV = 0x00000040
    JOY_RETURNBUTTONS = 0x00000080
    JOY_RETURNRAWDATA = 0x00000100
    JOY_RETURNPOVCTS = 0x00000200
    JOY_RETURNCENTERED = 0x00000400
    JOY_USEDEADZONE = 0x00000800
    JOY_RETURNALL = (JOY_RETURNX | JOY_RETURNY | JOY_RETURNZ |
                     JOY_RETURNR | JOY_RETURNU | JOY_RETURNV |
                     JOY_RETURNPOV | JOY_RETURNBUTTONS)

    def __init__(self, buffer):
        ushort_array = (ctypes.c_uint16 * 2).from_buffer(buffer)
        self.wMid, self.wPid = ushort_array

        wchar_array = (ctypes.c_wchar * 32).from_buffer(buffer, 4)
        self.szPname = ctypes.cast(wchar_array, ctypes.c_wchar_p).value

        uint_array = (ctypes.c_uint32 * 19).from_buffer(buffer, JOYCAPS.OFFSET_V)
        self.wXmin, self.wXmax, self.wYmin, self.wYmax, self.wZmin, self.wZmax, \
            self.wNumButtons, self.wPeriodMin, self.wPeriodMax, \
            self.wRmin, self.wRmax, self.wUmin, self.wUmax, self.wVmin, self.wVmax, \
            self.wCaps, self.wMaxAxes, self.wNumAxes, self.wMaxButtons = uint_array


class JOYINFOEX:
    SIZE = 52

    def __init__(self, buffer):
        uint_array = (ctypes.c_uint32 * (JOYINFOEX.SIZE // 4)).from_buffer(buffer)
        self.dwSize, self.dwFlags, \
            self.dwXpos, self.dwYpos, self.dwZpos, self.dwRpos, self.dwUpos, self.dwVpos, \
            self.dwButtons, self.dwButtonNumber, self.dwPOV, self.dwReserved1, self.dwReserved2 = uint_array
