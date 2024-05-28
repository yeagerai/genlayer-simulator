import random


class ConsensusValidators:
    def select_random_validators(
        self, all_validators: list, num_validators: int
    ) -> list:
        weights = []
        for i in all_validators:
            weights.append(float(i["stake"]))

        weighted_indices = random.choices(
            range(len(all_validators)), weights=weights, k=num_validators * 10
        )
        unique_indices = set()
        random.shuffle(weighted_indices)

        for idx in weighted_indices:
            unique_indices.add(idx)
            if len(unique_indices) == num_validators:
                break

        return [all_validators[i] for i in unique_indices]

    def get_validators_for_transaction(
        self, all_validators: list, num_validators: int
    ) -> tuple:
        selected_validators = self.select_random_validators(
            all_validators, num_validators
        )
        leader = selected_validators[0]
        remaining_validators = selected_validators[1 : num_validators + 1]
        return leader, remaining_validators
