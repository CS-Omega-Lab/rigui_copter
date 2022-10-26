from rich.console import Console


class LogManager:
    def __init__(self):
        self.cls = Console()

    def dlg(self, src, m_type, message):
        if m_type == 0:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][white bold]INFO[/][red bold]::[/]" + message)
        elif m_type == 1:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][red bold]ERROR[/][red bold]::[/]" + message)
        elif m_type == 2:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][yellow bold]WARN[/][red bold]::[/]" + message)
        elif m_type == 3:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][purple bold]INIT[/][red bold]::[/]" + message)
        else:
            self.cls.print("[blue bold]\[" + src + "][/][red bold]::[/][white bold]UNKNOWN[/][red bold]::[/]" + message)
