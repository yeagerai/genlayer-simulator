import os
import json
from logging.config import dictConfig
from loguru import logger
import sys

from backend.protocol_rpc.message_handler.types import LogEvent

MAX_LOG_MESSAGE_LENGTH = 3000


def setup_logging_config():
    logging_env = os.environ["LOGCONFIG"]
    file_path = (
        f"backend/protocol_rpc/message_handler/config/logging.{logging_env}.json"
    )
    with open(file_path, "r") as file:
        logging_config = json.load(file)
        dictConfig(logging_config)

    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<level>{level: <8}</level> | {message}",
    )


class MessageHandler:
    def __init__(self, socketio):
        self.socketio = socketio
        setup_logging_config()

    def socket_emit(self, log_event: LogEvent):
        self.socketio.emit(log_event.name, log_event.to_dict())

    def log_message(self, log_event: LogEvent):
        logging_status = log_event.type.value

        if not hasattr(logger, logging_status):
            logging_status = "info"

        log_method = getattr(logger, logging_status)

        message = (
            (log_event.message[:MAX_LOG_MESSAGE_LENGTH] + "...")
            if log_event.message is not None
            and len(log_event.message) > MAX_LOG_MESSAGE_LENGTH
            else log_event.message
        )

        log_message = f"[{log_event.scope.value}] {message}"
        gray = "\033[38;5;245m"
        reset = "\033[0m"

        if log_event.data:
            try:
                data_str = json.dumps(log_event.data, default=lambda o: o.__dict__)
                log_message += f" {gray}{data_str}{reset}"
            except TypeError as e:
                log_message += (
                    f" {gray}{str(log_event.data)} (serialization error: {e}){reset}"
                )

        log_method(log_message)

    def send_message(self, log_event: LogEvent):
        self.log_message(log_event)
        self.socket_emit(log_event)
