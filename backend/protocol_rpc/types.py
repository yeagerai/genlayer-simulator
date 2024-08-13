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
