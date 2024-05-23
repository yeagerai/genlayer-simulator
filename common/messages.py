import inspect
import traceback
import random
import string


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
        self.function = inspect.stack()[1].function
        self.trace_id = "".join(
            random.choice(string.digits + string.ascii_lowercase) for _ in range(9)
        )
        self.previous_log_level = self.app.logger.level
        self.response_format("info", message="Starting...")

    def debug_response(self, info_message, data) -> dict:
        self.response_format("debug", message=info_message, data=data)

    def info_response(self, info_message) -> dict:
        self.response_format("info", message=info_message)

    def error_response(self, message: str = "", exception=None) -> dict:
        if exception:
            return self.response_format(
                "error", str(exception), {"traceback": traceback.format_exc()}
            )
        return self.response_format("error", message=message)

    def success_response(self, data) -> dict:
        return self.response_format("success", data=data)

    def response_format(self, status: str, message: str = "", data={}) -> dict:
        result = {"status": status, "message": message, "data": data}
        logger_result = {
            "function": self.function,
            "trace_id": self.trace_id,
            "response": result,
        }
        # Will log the message at level = "status"
        logging_status = self.status_mappings[status]
        if hasattr(self.app.logger, logging_status):
            log_method = getattr(self.app.logger, logging_status)
            log_method(self.function + ": " + str(result))
        else:
            raise Exception(f"Logger does not have the method {status}")
        self.socketio_log(logger_result)
        return result

    def socketio_log(self, message):
        self.socketio.emit("status_update", {"message": message})
