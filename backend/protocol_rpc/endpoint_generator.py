# rpc/endpoint_generator.py
import traceback
from functools import partial, wraps
from typing import Callable
from flask_jsonrpc import JSONRPC

from backend.protocol_rpc.configuration import GlobalConfiguration
from backend.protocol_rpc.message_handler.base import MessageHandler
from backend.protocol_rpc.types import EndpointResult, EndpointResultStatus


def generate_rpc_endpoint(
    jsonrpc: JSONRPC,
    msg_handler: MessageHandler,
    config: GlobalConfiguration,
    function: Callable,
) -> Callable:
    @jsonrpc.method(function.__name__)
    @wraps(function)
    def endpoint(*args, **kwargs):
        shouldPrintInfoLogs = (
            function.__name__ not in config.get_disabled_info_logs_endpoints()
        )
        send_message = partial(msg_handler.send_message, function.__name__)
        if shouldPrintInfoLogs:
            send_message(EndpointResult(EndpointResultStatus.INFO, "Starting..."))

        try:
            function_result = function(*args, **kwargs)
            result = EndpointResult(
                EndpointResultStatus.SUCCESS,
                f"Endpoint {function.__name__} successfully executed",
                function_result,
            )
            if shouldPrintInfoLogs:
                send_message(result)
            return result.to_json()
        except Exception as e:
            result = EndpointResult(
                EndpointResultStatus.ERROR,
                f"Error executing endpoint {function.__name__}: {str(e)}",
                {"traceback": traceback.format_exc()},
                e,
            )
            send_message(result)
            return result.to_json()

    return endpoint


def generate_rpc_endpoint_for_partial(
    partial_generator: Callable, function: Callable, *args
) -> Callable:
    partial_function = partial(function, *args)
    partial_function.__name__ = function.__name__
    partial_function.__annotations__ = {
        k: v
        for k, v in function.__annotations__.items()
        if k not in list(function.__annotations__)[: len(args)]
    }
    return partial_generator(partial_function)
