from enum import Enum
from dataclasses import dataclass


class EventType(Enum):
    DEBUG = "debug"
    INFO = "info"
    SUCCESS = "success"
    ERROR = "error"


class EventScope(Enum):
    RPC = "RPC"
    GENVM = "GenVM"
    CONSENSUS = "Consensus"


@dataclass
class LogEvent:
    name: str
    type: EventType
    scope: EventScope
    message: str
    data: dict | None = None
    client_session_id: str | None = None

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type.value,
            "scope": self.scope.value,
            "message": self.message,
            "data": self.data,
            "client_id": self.client_session_id,
        }
