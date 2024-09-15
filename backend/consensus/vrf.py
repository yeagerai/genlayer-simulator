import numpy as np

rng = np.random.default_rng()


def get_validators_for_transaction(
    all_validators: list[dict], num_validators: int
) -> tuple:
    num_validators = min(num_validators, len(all_validators))

    total_stake = sum(validator["stake"] for validator in all_validators)
    probabilities = [validator["stake"] / total_stake for validator in all_validators]

    selected_validators = rng.choice(
        all_validators,
        p=probabilities,
        size=num_validators,
        replace=False,
    )

    leader = selected_validators[0]
    remaining_validators = selected_validators[1 : num_validators + 1]
    return leader, remaining_validators
