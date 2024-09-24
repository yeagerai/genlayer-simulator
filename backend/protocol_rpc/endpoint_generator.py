# rpc/endpoint_generator.py
import traceback
from functools import partial, wraps
from typing import Callable
from flask_jsonrpc import JSONRPC

from backend.protocol_rpc.configuration import GlobalConfiguration
from backend.protocol_rpc.message_handler.base import (
    LogEvent,
    EventType,
    EventScope,
    MessageHandler,
)
from backend.protocol_rpc.types import EndpointResult, EndpointResultStatus


def generate_rpc_endpoint(
    jsonrpc: JSONRPC,
    msg_handler: MessageHandler,
    config: GlobalConfiguration,
    function: Callable,
) -> Callable:
    @jsonrpc.method(function.__name__)
    @wraps(function)
    def endpoint(*args, **kwargs) -> dict[str]:
        shouldPrintInfoLogs = (
            function.__name__ not in config.get_disabled_info_logs_endpoints()
        )

        if shouldPrintInfoLogs:
            msg_handler.send_message(
                LogEvent(
                    "endpoint_call",
                    EventType.INFO,
                    EventScope.RPC,
                    "Calling endpoint: " + function.__name__,
                    {"endpoint_name": function.__name__, "args": args},
                )
            )

        try:
            function_result = function(*args, **kwargs)
            result = EndpointResult(
                EndpointResultStatus.SUCCESS,
                f"Success: {function.__name__}",
                function_result,
            )
            if shouldPrintInfoLogs:
                msg_handler.send_message(
                    LogEvent(
                        "endpoint_success",
                        EventType.SUCCESS,
                        EventScope.RPC,
                        "Endpoint responded: " + function.__name__,
                        {
                            "endpoint_name": function.__name__,
                            "result": function_result,
                        },
                    )
                )
            return result.to_json()

        except Exception as e:
            result = EndpointResult(
                EndpointResultStatus.ERROR,
                f"Error executing endpoint {function.__name__}: {str(e)}",
                {"traceback": traceback.format_exc()},
                e,
            )
            msg_handler.send_message(
                LogEvent(
                    "endpoint_error",
                    EventType.ERROR,
                    EventScope.RPC,
                    f"Error executing endpoint {function.__name__}: {str(e)}",
                    {
                        "endpoint_name": function.__name__,
                        "error": str(e),
                        "traceback": traceback.format_exc(),
                    },
                )
            )
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
