# rpc/endpoint_generator.py

from typing import Callable
from flask_jsonrpc import JSONRPC
from flask_jsonrpc.exceptions import JSONRPCError

from backend.protocol_rpc.message_handler.base import MessageHandler


def generate_rpc_endpoint(
    jsonrpc: JSONRPC,
    msg_handler: MessageHandler,
    function: Callable,
    method_name: str = "",
    *args: list,
    **kwargs: dict,
) -> Callable:
    json_rpc_method_name = function.__name__ if method_name is None else method_name

    @jsonrpc.method(json_rpc_method_name)
    @msg_handler.log_endpoint_info
    def endpoint():
        try:
            return function(*args, **kwargs)
        except Exception as e:
            raise JSONRPCError(code=-32000, message=str(e))

    return endpoint
