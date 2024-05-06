import os
import json
import logging
from logging.config import dictConfig
from colorama import init, Fore

init(autoreset=True)


def setup_logging_config():
    logging_env = os.environ['LOGCONFIG']
    file_path = f'common/config/logging.{logging_env}.json'
    with open(file_path, 'r') as file:
        logging_config = json.load(file)
        dictConfig(logging_config)


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