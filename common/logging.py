import logging
from colorama import init, Fore

init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Fore.WHITE
    }

    def format(self, record):
        log_level_color = self.COLORS.get(record.levelname, Fore.WHITE)
        log_message = super().format(record)
        return f"{log_level_color}{log_message}"