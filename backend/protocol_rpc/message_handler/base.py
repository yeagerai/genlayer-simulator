from enum import Enum
import os
import json
from logging.config import dictConfig
from dataclasses import dataclass
from loguru import logger
import sys

MAX_LOG_MESSAGE_LENGTH = 3000


def setup_logging_config():
    ## TODO: Remove config?
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
        # <white>{time:YYYY-MM-DD HH:mm:ss.SSS}</white>
        format="<level>{level: <8}</level> | {message}",
    )


## TODO: make sure all print to terminal as well
## TODO: print errors and tracebacks to terminal


## TODO: move to types files
class EventType(Enum):
    DEBUG = "debug"
    INFO = "info"
    SUCCESS = "success"
    ERROR = "error"


class EventScope(Enum):
    RPC = "RPC"
    GENVM = "GenVM"
    CONSENSUS = "Consensus"


@dataclass
class LogEvent:
    name: str
    type: EventType
    scope: EventScope
    message: str
    data: dict = None

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type.value,
            "scope": self.scope.value,
            "message": self.message,
            "data": self.data,
        }


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

        # Truncate the message if it exceeds MAX_LOG_MESSAGE_LENGTH
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
                # Try to JSON serialize the data and add it to the log message
                data_str = json.dumps(log_event.data, default=lambda o: o.__dict__)
                log_message += f" {gray}{data_str}{reset}"
            except TypeError as e:
                # If serialization fails, add the string representation of data and the error
                log_message += (
                    f" {gray}{str(log_event.data)} (serialization error: {e}){reset}"
                )

        # Log the constructed message using the appropriate logging method
        log_method(log_message)

    def send_message(self, log_event: LogEvent):
        self.log_message(log_event)
        self.socket_emit(log_event)
