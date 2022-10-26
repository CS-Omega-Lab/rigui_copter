import random
import re
import subprocess
import time
from threading import Thread
import pythonping


class TelemetryManager:
    def __init__(self, rdm, lgm):
        self.rdm = rdm
        self.lgm = lgm
        self.telemetry = [
            100,  # Уровень сигнала
            1,    # Пинг
            100,  # Заряд аккумулятора
            100,  # Температура
            100   # Ток
        ]

        self.thread = Thread(target=self.update, daemon=True, args=())

    def start(self):
        self.thread.start()
        return self

    def get_telemetry(self):
        return self.telemetry

    def update(self):
        while True:
            # p = subprocess.Popen("iwconfig", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # out = p.stdout.read().decode()
            # m = re.findall('(wlan1+).*?Signal level=()', out, re.DOTALL)
            # print(m)
            # signal_level = int(abs(m[0]))
            signal_level = 0

            response_list = pythonping.ping(self.rdm.config['network']['host'], size=10, count=2)
            ping = response_list.rtt_avg_ms
            if ping > 255:
                ping = 255
            signal_ping = int(ping)

            battery_charge = 100

            # p = subprocess.Popen("vcgencmd measure_temp", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # out = p.stdout.read().decode()
            # m = re.findall(r'\d+', out)
            # soc_temperature = m[0]
            soc_temperature = 0

            motor_summary = self.rdm.get_motors_summary()
            diff = abs(motor_summary) / 10
            load_current = int(diff)

            self.telemetry = [
                signal_level,
                signal_ping,
                battery_charge,
                soc_temperature,
                load_current
            ]

            time.sleep(0.2)
