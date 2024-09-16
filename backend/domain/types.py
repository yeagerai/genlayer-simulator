# Types from our domain
# Trying to follow [hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) or layered architecture.
# These types should not depend on any other layer.

from dataclasses import dataclass
import decimal
from enum import Enum

from backend.database_handler.models import TransactionStatus


@dataclass()
class LLMProvider:
    provider: str
    model: str
    config: dict
    plugin: str
    plugin_config: dict
    id: int | None = None

    def __hash__(self):
        return hash(
            (
                self.id,
                self.provider,
                self.model,
                frozenset(self.config.items()),
                frozenset(self.plugin_config.items()),
            )
        )


@dataclass()
class Validator:
    address: str
    stake: int
    llmprovider: LLMProvider
    id: int | None = None

    def to_dict(self):
        result = {
            "address": self.address,
            "stake": self.stake,
            "provider": self.llmprovider.provider,
            "model": self.llmprovider.model,
            "config": self.llmprovider.config,
            "plugin": self.llmprovider.plugin,
            "plugin_config": self.llmprovider.plugin_config,
        }

        if self.id:
            result["id"] = self.id

        return result


class TransactionType(Enum):
    SEND = 0
    DEPLOY_CONTRACT = 1
    RUN_CONTRACT = 2


@dataclass
class Transaction:
    hash: str
    status: TransactionStatus
    type: TransactionType
    from_address: str | None = None
    to_address: str | None = None
    input_data: dict | None = None
    data: dict | None = None
    consensus_data: dict | None = None
    nonce: int | None = None
    value: decimal.Decimal | None = None
    gaslimit: int | None = None
    r: int | None = None
    s: int | None = None
    v: int | None = None


def transaction_from_dict(input: dict) -> Transaction:
    return Transaction(
        hash=input["hash"],
        status=TransactionStatus(input["status"]),
        type=TransactionType(input["type"]),
        from_address=input["from_address"],
        to_address=input["to_address"],
        input_data=input["input_data"],
        data=input["data"],
        consensus_data=input["consensus_data"],
        nonce=input["nonce"],
        value=input["value"],
        gaslimit=input["gaslimit"],
        r=input["r"],
        s=input["s"],
        v=input["v"],
    )
