from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional
import base64


class Address:
    SIZE = 32
    _as_bytes: bytes

    def __init__(self, val: str | bytes | memoryview):
        if isinstance(val, memoryview):
            val = bytes(val)
        if isinstance(val, str) or len(val) > Address.SIZE:
            val = base64.b64decode(val)
        if len(val) != Address.SIZE:
            raise Exception("invalid address")
        self._as_bytes = val

    @property
    def as_bytes(self) -> bytes:
        return self._as_bytes

    @property
    def as_int(self) -> int:
        return int.from_bytes(self._as_bytes, "little", signed=False)

    def __hash__(self):
        return hash(self._as_bytes)

    def __eq__(self, r):
        if not isinstance(r, Address):
            return False
        return self._as_bytes == r._as_bytes

    def __repr__(self) -> str:
        return "addr:[" + "".join(["{:02x}".format(x) for x in self._as_bytes]) + "]"


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
    calldata: bytes

    def to_dict(self):
        return {
            "address": self.address,
            "calldata": str(base64.b64encode(self.calldata), encoding="ascii"),
        }


@dataclass
class Receipt:
    class_name: str
    calldata: bytes
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
            "calldata": str(base64.b64encode(self.calldata), encoding="ascii"),
            "gas_used": self.gas_used,
            "mode": self.mode.value,
            "contract_state": self.contract_state,
            "node_config": self.node_config,
            "eq_outputs": self.eq_outputs,
            "error": str(self.error) if self.error else None,
            "pending_transactions": [
                pending_transaction.to_dict()
                for pending_transaction in self.pending_transactions
            ],
        }
