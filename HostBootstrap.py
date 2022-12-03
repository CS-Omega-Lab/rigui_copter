import time
import os
import configparser

from rich import box
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from Host.HostDataManager import DataManager
from Common.LogManager import LogManager
from Common.ConstStorage import ConstStorage as CS


def make_layout(n) -> Layout:
    page = Layout(name="root")
    page.split(
        Layout(name="header", size=3),
        Layout(name="info", size=8),
        Layout(name="logs", size=(n - 11)),
    )
    page["info"].split_row(
        Layout(name="state"),
        Layout(name="telemetry"),
    )
    return page


class Header:
    @staticmethod
    def __rich__() -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b] [Powered by EXPLORA] RiGUI Robot Control V5.1.0"
        )
        return Panel(grid,
                     border_style="bright_blue",
                     style="white bold")


class State:
    def __init__(self, prv):
        self.vals = prv.get_vals()

    def __rich__(self) -> Panel:
        content = Text()

        content.append("Режим: ", style="bold green")
        if self.vals[5] == CS.MIN_VAL:
            content.append("РУЧНОЙ\r\n", style="bold blue u")
        elif self.vals[5] == CS.MID_VAL:
            content.append("GPS (3D FIX)\r\n", style="bold blue u")
        else:
            content.append("АВТО\r\n", style="bold blue u")

        content.append("Моторы: ", style="bold green")

        if self.vals[4] == CS.MIN_VAL:
            content.append("DISARMED\r\n", style="bold gray u")
        else:
            content.append("ARMED\r\n", style="bold blue u")

        content_panel = Panel(
            Align.left(
                content,
                vertical="top"
            ),
            box=box.ROUNDED,
            padding=(0, 1, 0, 1),
            title="[b red] Режимы управления",
            border_style="bright_blue",
        )
        return content_panel


class Telemetry:
    def __init__(self, prv):
        self.data = prv.get_telemetry()

    def __rich__(self) -> Panel:
        content = Text()
        content.append("Уровень сигнала связи: ", style="bold green")
        content.append(str(self.data[0]) + "%\r\n")
        content.append("Время отклика:         ", style="bold green")
        content.append(str(self.data[1]) + " мс\r\n")
        content.append("Заряд аккумулятора:    ", style="bold green")
        content.append(str(self.data[2]) + "%\r\n")
        content.append("Температура SoC:       ", style="bold green")
        content.append(str(self.data[3]) + " °C\r\n")
        content.append("Ток в силовой цепи:    ", style="bold green")
        content.append(str(self.data[4]) + " А\r\n")
        content_panel = Panel(
            Align.left(
                content,
                vertical="top"
            ),
            box=box.ROUNDED,
            padding=(0, 1, 0, 1),
            title="[b red] Данные телеметрии",
            border_style="bright_blue",
        )
        return content_panel


class Logs:
    def __init__(self, prv):
        self.logs = prv.get_logs()

    def __rich__(self) -> Panel:
        content = Text.from_markup(
            self.logs
        )
        content_panel = Panel(
            Align.left(
                content,
                vertical="bottom"
            ),
            box=box.ROUNDED,
            padding=(0, 2),
            title="[b red] Логи",
            border_style="bright_blue",
        )
        return content_panel


lgm = LogManager()
lgm.dlg('HOST', 3, 'Запускаюсь...')
config = configparser.ConfigParser()
config.read("Assets/explora.cfg")
rows = os.get_terminal_size()[1]
data_manager = DataManager(config, lgm, rows).start()
while data_manager.in_waiting():
    time.sleep(0.1)
os.system('cls')
layout = make_layout(rows)
layout["header"].update(Header())
layout["logs"].update(Logs(data_manager))
layout["state"].update(State(data_manager))
layout["telemetry"].update(Telemetry(data_manager))

with Live(layout, refresh_per_second=100, screen=True):
    while True:
        time.sleep(0.01)
        layout["logs"].update(Logs(data_manager))
        layout["state"].update(State(data_manager))
        layout["telemetry"].update(Telemetry(data_manager))
