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
            0,  # Уровень сигнала
            0,    # Пинг
            0,  # Заряд аккумулятора
            0,  # Температура
            0   # Ток
        ]
        self.host = ''

        self.thread = Thread(target=self.update, daemon=True, args=())

    def start(self, host):
        self.host = host
        self.thread.start()
        return self

    def get_telemetry(self):
        return self.telemetry

    def update(self):
        while True:
            signal_level = 0

            response_list = pythonping.ping(self.host, size=10, count=2)
            ping = response_list.rtt_avg_ms
            if ping > 255:
                ping = 255
            signal_ping = int(ping)

            battery_charge = 100
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

            time.sleep(0.1)
