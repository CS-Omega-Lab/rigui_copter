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
from Host.HostDataManager import DataManager as DM


def make_layout(n) -> Layout:
    page = Layout(name="root")
    page.split(
        Layout(name="header", size=3),
        Layout(name="state", size=8),
        Layout(name="logs", size=(n - 11)),
    )
    return page


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


class Mode:
    def __init__(self, prv):
        self.mode = prv.get_mode()
        self.vals = prv.get_vals()

    def __rich__(self) -> Panel:
        content = Text()

        content.append("Контроль робота: ", style="bold green")
        if not self.mode[0]:
            content.append("ПОЛУАВТОМАТИЧЕСКИЙ\r\n", style="bold blue u")
            content.append("    Состояние камеры: ", style="bold green")
            if self.vals[4][0] > 127:
                content.append("X↑ ", style="bold blue")
            elif self.vals[4][0] < 127:
                content.append("X↓ ", style="bold blue")
            else:
                content.append("X· ", style="bold white")
            if self.vals[4][1] > 127:
                content.append("Y↑\r\n", style="bold blue")
            elif self.vals[4][1] < 127:
                content.append("Y↓\r\n", style="bold blue")
            else:
                content.append("Y·\r\n", style="bold white")

            content.append("    Скорость:      ", style="bold green")
            content.append(str(self.mode[2] - 27) + "% \r\n")
            content.append("    Пресет:        ", style="bold green")
            content.append(str(self.mode[3]+1) + "\r\n")
            content.append("    Длительность:  ", style="bold green")
            content.append(str(self.mode[4]) + "с \r\n")
        else:
            content.append("РУЧНОЙ\r\n", style="bold blue u")
            content.append("Состояние камеры: ", style="bold green")
            if self.vals[4][0] > 127:
                content.append("X↑ ", style="bold blue")
            elif self.vals[4][0] < 127:
                content.append("X↓ ", style="bold blue")
            else:
                content.append("X· ", style="bold white")
            if self.vals[4][1] > 127:
                content.append("Y↑\r\n", style="bold blue")
            elif self.vals[4][1] < 127:
                content.append("Y↓\r\n", style="bold blue")
            else:
                content.append("Y·\r\n", style="bold white")
            content.append("Режим управления: ", style="bold green")
            if self.mode[1]:
                content.append("ШАССИ", style="bold blue u")
                content.append(" ")
                content.append("МАНИПУЛЯТОР\r\n", style="white")
                content.append("    Скорость:            ", style="bold green")
                content.append(str(self.mode[2] - 27) + "% \r\n")
                content.append("    Состояние гусениц:   ", style="bold green")
                if self.vals[0][0] > 127:
                    if self.vals[0][0] != self.mode[2] + 127:
                        content.append("↑ ", style="bold yellow")
                    else:
                        content.append("↑ ", style="bold blue")
                elif self.vals[0][0] < 127:
                    if self.vals[0][0] != 127 - self.mode[2]:
                        content.append("↓ ", style="bold yellow")
                    else:
                        content.append("↓ ", style="bold blue")
                else:
                    content.append("· ", style="bold white")

                if self.vals[0][1] > 127:
                    if self.vals[0][1] != self.mode[2] + 127:
                        content.append("↑\r\n", style="bold yellow")
                    else:
                        content.append("↑\r\n", style="bold blue")
                elif self.vals[0][1] < 127:
                    if self.vals[0][1] != 127 - self.mode[2]:
                        content.append("↓\r\n", style="bold yellow")
                    else:
                        content.append("↓\r\n", style="bold blue")
                else:
                    content.append("·\r\n", style="bold white")

                content.append("    Состояние плавников: ", style="bold green")

                if self.vals[1][0] > 127:
                    content.append("↑ ", style="bold blue")
                elif self.vals[1][0] < 127:
                    content.append("↓ ", style="bold blue")
                else:
                    content.append("· ", style="bold white")

                if self.vals[1][1] > 127:
                    content.append("↑\r\n", style="bold blue")
                elif self.vals[1][1] < 127:
                    content.append("↓\r\n", style="bold blue")
                else:
                    content.append("·\r\n", style="bold white")
            else:
                content.append("ШАССИ ", style="white")
                content.append("МАНИПУЛЯТОР\r\n", style="bold blue u")
                content.append("    Текущая ось: ", style="bold green")
                content.append(str(self.vals[2]) + "\r\n")
                content.append("    Состояние оси: ", style="bold green")
                if self.vals[3] > 127:
                    content.append("↑\r\n", style="bold blue")
                elif self.vals[3] < 127:
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


class Header:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b] EXPLORA Robot Control V1.8"
        )
        return Panel(grid,
                     border_style="bright_blue",
                     style="white bold")


config = configparser.ConfigParser()
config.read("assets/explora.cfg")
rows = os.get_terminal_size()[1]
provider = DM(config, rows).start()
layout = make_layout(rows)
layout["header"].update(Header())
layout["logs"].update(Logs(provider))
layout["state"].update(Mode(provider))

with Live(layout, refresh_per_second=100, screen=True):
    while True:
        time.sleep(0.01)
        layout["logs"].update(Logs(provider))
        layout["state"].update(Mode(provider))
