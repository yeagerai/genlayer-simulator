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
            "leader_receipt": {
                "vote": self.leader_receipt.vote.value,
                "execution_result": self.leader_receipt.execution_result.value,
                "class_name": self.leader_receipt.class_name,
                "method": self.leader_receipt.method,
                "args": self.leader_receipt.args,
                "gas_used": self.leader_receipt.gas_used,
                "mode": self.leader_receipt.mode.value,
                "contract_state": self.leader_receipt.contract_state,
                "node_config": self.leader_receipt.node_config,
                "eq_outputs": self.leader_receipt.eq_outputs,
                "error": (
                    str(self.leader_receipt.error)
                    if self.leader_receipt.error
                    else None
                ),
            },
            "validators": [receipt.to_dict() for receipt in self.validators],
        }
