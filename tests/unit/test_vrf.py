from backend.consensus.vrf import get_validators_for_transaction


def test_get_validators_for_transaction():
    validators = [{"stake": 1}, {"stake": 2}, {"stake": 3}]
    result = get_validators_for_transaction(validators, 10)

    assert set(result) == set(validators)

    print(result)


def test_get_validators_for_transaction_2():
    validators = [{"stake": 1}, {"stake": 2}, {"stake": 3}]

    validators_set = set(validators)

    accumulated = set()
    while True:
        result = get_validators_for_transaction(validators, 2)
        print(result)
        accumulated.update(set(result))

        if accumulated == set(validators_set):
            break
