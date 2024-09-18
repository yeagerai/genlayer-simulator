import traceback
import random
import string
import os
import json
from functools import wraps, partial
from logging.config import dictConfig

from backend.protocol_rpc.message_handler.types import FormattedResponse
from backend.protocol_rpc.types import EndpointResult, EndpointResultStatus

MAX_LOG_MESSAGE_LENGTH = 3000


def log_endpoint_info_wrapper(msg_handler, config):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            shouldPrintInfoLogs = (
                func.__name__ not in config.get_disabled_info_logs_endpoints()
            )
            send_message = partial(msg_handler.send_message, func.__name__)

            if shouldPrintInfoLogs:
                send_message(EndpointResult(EndpointResultStatus.INFO, "Starting..."))

            try:
                result = func(*args, **kwargs)
                if shouldPrintInfoLogs:
                    send_message(
                        EndpointResult(
                            EndpointResultStatus.SUCCESS,
                            f"Endpoint {func.__name__} successfully executed",
                            result,
                        )
                    )
                return result
            except Exception as e:
                send_message(
                    EndpointResult(
                        EndpointResultStatus.ERROR,
                        f"Error executing endpoint {func.__name__}: {str(e)}",
                        {"traceback": traceback.format_exc()},
                        e,
                    )
                )
                raise e

        return wrapper

    return decorator


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


class MessageHandler:

    status_mappings = {
        "debug": "info",
        "info": "info",
        "success": "info",
        "error": "error",
    }

    def __init__(self, app, socketio, config):
        self.app = app
        self.socketio = socketio
        self.config = config
        setup_logging_config()

    def log_endpoint_info(self, func):
        return log_endpoint_info_wrapper(self, self.config)(func)

    def socket_emit(self, message):
        self.socketio.emit("status_update", {"message": message})

    def log_message(self, function_name, result: EndpointResult):
        logging_status = self.status_mappings[result.status.value]
        if hasattr(self.app.logger, logging_status):
            log_method = getattr(self.app.logger, logging_status)
            result_string = str(result)
            function_result = (
                (result_string[:MAX_LOG_MESSAGE_LENGTH] + "...")
                if result_string is not None
                and len(result_string) > MAX_LOG_MESSAGE_LENGTH
                else result_string
            )
            log_method(function_name + ": " + function_result)
        else:
            raise Exception(f"Logger does not have the method {result.status}")

    def send_message(
        self,
        function_name: str,
        result: EndpointResult,
    ):
        self.log_message(function_name, result)

        formatted_response = format_response(function_name, result)
        self.socket_emit(formatted_response.to_json())
