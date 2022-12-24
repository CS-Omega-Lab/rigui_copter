import time
from threading import Thread
import pythonping


class TelemetryManager:
    def __init__(self, rdm, lgm):
        self.rdm = rdm
        self.lgm = lgm
        self.started = False
        self.telemetry = [
            0,  # Пинг
            0,  # Состояние ошибки
        ]
        self.host = ''

        self.thread = Thread(target=self.update, daemon=True, args=())

    def start(self, host):
        self.host = host
        if not self.started:
            self.thread.start()
            self.started = True
        return self

    def get_telemetry(self):
        return self.telemetry

    def update(self):
        while True:
            response_list = pythonping.ping(self.host, size=10, count=1)
            ping = response_list.rtt_avg_ms
            if ping > 255:
                ping = 255
            signal_ping = int(ping)
            self.telemetry = [
                signal_ping,
                0
            ]
            time.sleep(0.1)
