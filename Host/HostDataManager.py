import time
from threading import Thread

from Host.HostNetworkClient import NetworkClient as NC
from Host.Drivers.Keyboard import Keyboard as KC
from Host.ManualCameraReader import ManualCameraReader as MCR


class DataManager:
    def __init__(self, config, rows):
        self.log_list = ''''''
        self.log_ctr = 0
        self.rows = rows
        self.config = config

        # mode,         [0][1]
        # motor_params, [1][2]
        # fin_params,   [2][2]
        # max_speed,    [3][1]
        # current_axis, [4][1]
        # axis_params,  [5][1]

        self.mode = [
            True,
            (127, 127),
            (127, 127),
            127,
            0,
            127
        ]
        self.thread = Thread(target=self.update, daemon=True, args=())
        self.lg('HOST', 0, 'Запуск DataManager: успешно.')
        self.keyboard_connector = KC(self, config['keyboard']).start()
        self.network_client = NC(self, config['general']).start()
        self.mcr = MCR(self).start()

    def get_logs(self):
        return self.log_list

    def get_mode(self):
        return self.mode

    def lg(self, src, typ, message):
        if typ == 0:
            self.log_list += "[blue bold]\[" + src + \
                             "][/][red bold]::[/][white bold]INFO[/][red bold]::[/]" + message + "\r\n"
        elif typ == 1:
            self.log_list += "[blue bold]\[" + src + \
                             "][/][red bold]::[/][red bold]ERROR[/][red bold]::[/]" + message + "\r\n"
        else:
            self.log_list += "[blue bold]\[" + src + \
                             "][/][red bold]::[/][yellow bold]WARN[/][red bold]::[/]" + message + "\r\n"
        self.log_ctr += 1
        if self.log_ctr >= self.rows - 4:
            idx = self.log_list.find('\r\n')
            self.log_list = self.log_list[idx + 1:]

    def start(self):
        self.thread.start()
        return self

    def update(self):
        while True:
            time.sleep(0.01)
            self.mode = self.keyboard_connector.get_state()

            # mode,         [0][1]
            # motor_params, [1][2]
            # fin_params,   [2][2]
            # current_axis, [3][1]
            # axis_params,  [4][1]

            self.network_client.send_info((
                self.mode[0],
                self.mode[1][0],
                self.mode[1][1],
                self.mode[2][0],
                self.mode[2][1],
                self.mode[4],
                self.mode[5]
            ))
