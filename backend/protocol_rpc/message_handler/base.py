from enum import Enum
import random
import string
import os
import json
from flask import Flask
from logging.config import dictConfig
from dataclasses import dataclass, asdict

from backend.protocol_rpc.message_handler.types import FormattedResponse
from backend.protocol_rpc.types import EndpointResult

MAX_LOG_MESSAGE_LENGTH = 3000


def setup_logging_config():
    logging_env = os.environ["LOGCONFIG"]
    file_path = (
        f"backend/protocol_rpc/message_handler/config/logging.{logging_env}.json"
    )
    with open(file_path, "r") as file:
        logging_config = json.load(file)
        dictConfig(logging_config)


def format_response(function_name: str, result: EndpointResult) -> FormattedResponse:
    trace_id = "".join(
        random.choice(string.digits + string.ascii_lowercase) for _ in range(9)
    )
    return FormattedResponse(function_name, trace_id, result)


## TODO: make sure all print to terminal as well
## TODO: print errors and tracebacks to terminal


## TODO: move to types files
class EventType(Enum):
    # DEBUG = "debug"
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
    # TODO: keep this?
    status_mappings = {
        "debug": "info",
        "info": "info",
        "success": "info",
        "error": "error",
    }

    def __init__(self, app: Flask, socketio):
        self.app = app
        self.socketio = socketio
        setup_logging_config()

    def socket_emit(self, log_event: LogEvent):
        self.socketio.emit(log_event.name, log_event.to_dict())

    ## TODO: use a library or salvage logic
    def log_message(self, log_event: LogEvent):
        print(
            f"{log_event.type.value} "
            f"{log_event.scope.value} "
            f"{log_event.name} "
            f"{log_event.message}"
        )
        # logging_status = self.status_mappings[log_event.type.value]
        # if hasattr(self.app.logger, logging_status):
        #     log_method = getattr(self.app.logger, logging_status)
        #     message = (
        #         (log_event.message[:MAX_LOG_MESSAGE_LENGTH] + "...")
        #         if log_event.message is not None
        #         and len(log_event.message) > MAX_LOG_MESSAGE_LENGTH
        #         else log_event.message
        #     )
        #     log_message = f"{log_event.name} [{log_event.scope.value}]: {message}"
        #     if log_event.data:
        #         try:
        #             log_message += f" | Data: {json.dumps(log_event.data, default=lambda o: o.__dict__)}"
        #         except TypeError as e:
        #             log_message += f" | Data: {str(log_event.data)} (serialization error: {e})"
        #     log_method(log_message)
        # else:
        #     raise Exception(f"Logger does not have the method {log_event.type.value}")

    def send_message(self, log_event: LogEvent):
        self.log_message(log_event)
        self.socket_emit(log_event)
