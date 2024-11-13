from dataclasses import dataclass
from backend.node.genvm.types import Receipt
from typing import Optional


@dataclass
class ConsensusData:
    final: bool
    votes: dict[str, str]
    leader_receipt: Receipt | None
    validators: list[Receipt] | None = None

    def to_dict(self):
        return {
            "final": self.final,
            "votes": self.votes,
            "leader_receipt": (
                self.leader_receipt.to_dict() if self.leader_receipt else None
            ),
            "validators": [receipt.to_dict() for receipt in self.validators],
        }

    @classmethod
    def from_dict(cls, input: dict) -> Optional["ConsensusData"]:
        if input:
            return cls(
                final=input.get("final", False),
                votes=input.get("votes", {}),
                leader_receipt=Receipt.from_dict(input.get("leader_receipt", None)),
                validators=[
                    Receipt.from_dict(validator)
                    for validator in (input.get("validators", None) or [])
                ],
            )
        else:
            return None
