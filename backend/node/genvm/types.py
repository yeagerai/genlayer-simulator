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

    @classmethod
    def from_string(cls, value: str) -> "Vote":
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid vote value: {value}")


class ExecutionMode(Enum):
    LEADER = "leader"
    VALIDATOR = "validator"

    @classmethod
    def from_string(cls, value: str) -> "ExecutionMode":
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid execution mode value: {value}")


class ExecutionResultStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    @classmethod
    def from_string(cls, value: str) -> "ExecutionResultStatus":
        try:
            return cls(value.upper())
        except ValueError:
            raise ValueError(f"Invalid execution result status value: {value}")


@dataclass
class PendingTransaction:
    address: str  # Address of the contract to call
    calldata: bytes

    def to_dict(self):
        return {
            "address": self.address,
            "calldata": str(base64.b64encode(self.calldata), encoding="ascii"),
        }

    @classmethod
    def from_dict(cls, input: dict) -> "PendingTransaction":
        return cls(
            address=input.get("address"),
            calldata=base64.b64decode(input.get("calldata")),
        )


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

    @classmethod
    def from_dict(cls, input: dict) -> Optional["Receipt"]:
        if input:
            return cls(
                vote=Vote.from_string(input.get("vote")),
                execution_result=ExecutionResultStatus.from_string(
                    input.get("execution_result")
                ),
                class_name=input.get("class_name"),
                calldata=base64.b64decode(input.get("calldata")),
                gas_used=input.get("gas_used"),
                mode=ExecutionMode.from_string(input.get("mode")),
                contract_state=input.get("contract_state"),
                node_config=input.get("node_config"),
                eq_outputs=input.get("eq_outputs"),
                error=Exception(input.get("error")) if input.get("error") else None,
                pending_transactions=tuple(
                    PendingTransaction.from_dict(pending_transaction)
                    for pending_transaction in input.get("pending_transactions", [])
                ),
            )
        else:
            return None
