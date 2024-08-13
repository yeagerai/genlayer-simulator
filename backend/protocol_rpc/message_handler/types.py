from dataclasses import dataclass

from backend.protocol_rpc.types import EndpointResult


@dataclass
class FormattedResponse:
    function_name: str
    trace_id: str
    response: EndpointResult

    def to_json(self):
        return {
            "function_name": self.function_name,
            "trace_id": self.trace_id,
            "response": self.response.to_json(),
        }
