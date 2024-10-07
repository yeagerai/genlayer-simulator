from dataclasses import dataclass
from backend.node.genvm.types import Receipt


@dataclass
class ConsensusData:
    final: bool
    votes: dict[str, str]
    leader_receipt: Receipt
    validators: list[Receipt] | None = None

    def to_dict(self):
        return {
            "final": self.final,
            "votes": self.votes,
            "leader_receipt": self.leader_receipt.to_dict(),
            "validators": [receipt.to_dict() for receipt in self.validators],
        }
