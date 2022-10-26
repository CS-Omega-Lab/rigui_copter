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
            "[b] EXPLORA Robot Control V4.2.0"
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
        content.append("РУЧНОЙ\r\n", style="bold blue u")
        content.append("Камера: ", style="bold green")
        if self.vals[3][0] > 127:
            content.append("H↑ ", style="bold blue")
        elif self.vals[3][0] < 127:
            content.append("H↓ ", style="bold blue")
        else:
            content.append("H· ", style="bold white")
        if self.vals[3][1] > 127:
            content.append("V↑\r\n", style="bold blue")
        elif self.vals[3][1] < 127:
            content.append("V↓\r\n", style="bold blue")
        else:
            content.append("V·\r\n", style="bold white")

        content.append("                 AX1: ", style="bold green")
        if self.vals[2][0] > 127:
            content.append("↑\r\n", style="bold blue")
        elif self.vals[2][0] < 127:
            content.append("↓\r\n", style="bold blue")
        else:
            content.append("·\r\n", style="bold white")

        content.append("Привод:   ", style="bold green")
        if self.vals[0][0] > 127:
            content.append("↑ ", style="bold blue")
        elif self.vals[0][0] < 127:
            content.append("↓ ", style="bold blue")
        else:
            content.append("· ", style="bold white")

        if self.vals[0][1] > 127:
            content.append("↑", style="bold blue")
        elif self.vals[0][1] < 127:
            content.append("↓", style="bold blue")
        else:
            content.append("·", style="bold white")

        content.append("    AX2: ", style="bold green")
        if self.vals[2][1] > 127:
            content.append("↑\r\n", style="bold blue")
        elif self.vals[2][1] < 127:
            content.append("↓\r\n", style="bold blue")
        else:
            content.append("·\r\n", style="bold white")

        content.append("Плавники: ", style="bold green")

        if self.vals[1][0] > 127:
            content.append("↑ ", style="bold blue")
        elif self.vals[1][0] < 127:
            content.append("↓ ", style="bold blue")
        else:
            content.append("· ", style="bold white")

        if self.vals[1][1] > 127:
            content.append("↑", style="bold blue")
        elif self.vals[1][1] < 127:
            content.append("↓", style="bold blue")
        else:
            content.append("·", style="bold white")

        content.append("    AX3: ", style="bold green")
        if self.vals[2][2] > 127:
            content.append("↑\r\n", style="bold blue")
        elif self.vals[2][2] < 127:
            content.append("↓\r\n", style="bold blue")
        else:
            content.append("·\r\n", style="bold white")

        content.append("                 AX4: ", style="bold green")
        if self.vals[2][3] > 127:
            content.append("↑\r\n", style="bold blue")
        elif self.vals[2][3] < 127:
            content.append("↓\r\n", style="bold blue")
        else:
            content.append("·\r\n", style="bold white")

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
config.read("assets/explora.cfg")
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
