import traceback
import random
import string
import os
import json
from logging.config import dictConfig

MAX_LOG_MESSAGE_LENGTH = 1000


def setup_logging_config():
    logging_env = os.environ["LOGCONFIG"]
    file_path = (
        f"backend/protocol_rpc/message_handler/config/logging.{logging_env}.json"
    )
    with open(file_path, "r") as file:
        logging_config = json.load(file)
        dictConfig(logging_config)


def format_response(function_name: str, result: dict) -> dict:
    formatted_response = {
        "function": function_name,
        "trace_id": "".join(
            random.choice(string.digits + string.ascii_lowercase) for _ in range(9)
        ),
        "response": result,
    }

    return formatted_response


class MessageHandler:

    status_mappings = {
        "debug": "info",
        "info": "info",
        "success": "info",
        "error": "error",
    }

    def __init__(self, app, socketio):
        self.app = app
        self.socketio = socketio
        setup_logging_config()

    def socket_emit(self, message):
        self.socketio.emit("status_update", {"message": message})

    def log_message(self, function_name, status, result):
        logging_status = self.status_mappings[status]
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
            raise Exception(f"Logger does not have the method {status}")

    def send_message(
        self,
        function_name: str,
        status: str,
        message: str = "",
        data={},
        exception=None,
    ):
        if exception:
            return self.send_message(
                function_name,
                "error",
                str(exception),
                {"traceback": traceback.format_exc()},
                None,
            )
        result = {"status": status, "message": message, "data": data}
        formatted_result = format_response(function_name, result)

        self.log_message(function_name, status, result)
        self.socket_emit(formatted_result)
        return result
