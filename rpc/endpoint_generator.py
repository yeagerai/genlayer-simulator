# rpc/endpoint_generator.py

from functools import partial, wraps
from typing import Callable
from flask_jsonrpc import JSONRPC
from message_handler.base import MessageHandler


def generate_rpc_endpoint(
    jsonrpc: JSONRPC, msg_handler: MessageHandler, function: Callable
) -> Callable:
    @jsonrpc.method(function.__name__)
    @wraps(function)
    def endpoint(*args, **kwargs):
        send_message = partial(msg_handler.send_message, function.__name__)
        send_message("info", "Starting...")
        try:
            result = function(*args, **kwargs)
            return send_message("success", data=result)
        except Exception as e:
            return send_message("error", exception=str(e))

    return endpoint
