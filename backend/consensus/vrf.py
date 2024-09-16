from datetime import datetime
import numpy as np


def get_validators_for_transaction(
    nodes: list[dict],
    num_validators: int,
    rng=np.random.default_rng(seed=int(datetime.now().timestamp())),
) -> tuple[dict, list[dict]]:
    num_validators = min(num_validators, len(nodes))

    total_stake = sum(validator["stake"] for validator in nodes)
    probabilities = [validator["stake"] / total_stake for validator in nodes]

    selected_validators = rng.choice(
        nodes,
        p=probabilities,
        size=num_validators,
        replace=False,
    )

    leader = selected_validators[0]
    remaining_validators = list(selected_validators[1 : num_validators + 1])
    return leader, remaining_validators
