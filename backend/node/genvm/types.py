from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Vote(Enum):
    AGREE = "agree"
    DISAGREE = "disagree"


class ExecutionMode(Enum):
    LEADER = "leader"
    VALIDATOR = "validator"


class ExecutionResultStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


@dataclass
class Receipt:
    class_name: str
    method: str
    args: list[str]
    gas_used: int
    mode: ExecutionMode
    contract_state: str
    node_config: dict
    eq_outputs: dict
    execution_result: ExecutionResultStatus
    error: Optional[Exception] = None
    vote: Optional[Vote] = None
