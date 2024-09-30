from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional


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
class PendingTransaction:
    address: str  # Address of the contract to call
    method_name: str
    args: list


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
    pending_transactions: Iterable[PendingTransaction] = ()

    def to_dict(self):
        return {
            "vote": self.vote.value,
            "execution_result": self.execution_result.value,
            "class_name": self.class_name,
            "method": self.method,
            "args": self.args,
            "gas_used": self.gas_used,
            "mode": self.mode.value,
            "contract_state": self.contract_state,
            "node_config": self.node_config,
            "eq_outputs": self.eq_outputs,
            "error": str(self.error) if self.error else None,
            "pending_transactions": [
                pending_transaction.__dict__
                for pending_transaction in self.pending_transactions
            ],
        }
