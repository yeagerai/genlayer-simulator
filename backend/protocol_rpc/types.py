from enum import Enum
from dataclasses import dataclass, field


class EndpointResultStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    INFO = "info"


@dataclass
class EndpointResult:
    status: EndpointResultStatus
    message: str
    data: dict = field(default_factory=dict)
    exception: Exception = None

    def to_json(self):
        return {
            "status": self.status.value,
            "message": self.message,
            "data": self.data,
            "exception": str(self.exception) if self.exception else None,
        }


@dataclass
class DecodedTransaction:
    from_address: str
    to_address: str
    data: str
    type: str
    value: int


@dataclass
class DecodedMethodCallData:
    function_name: str
    function_args: str


@dataclass
class DecodedDeploymentData:
    contract_code: str
    constructor_args: str
