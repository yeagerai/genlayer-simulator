from backend.consensus.vrf import get_validators_for_transaction


def list_of_dicst_to_set(list_of_dicts: list[dict]) -> set:
    return set(map(lambda x: tuple(x.items()), list_of_dicts))


def test_get_validators_for_transaction():
    """
    Tests that
    * correctly returns all nodes when asked for more validators than there are nodes
    * the order of the validators is random

    """
    nodes = [{"stake": 1}, {"stake": 2}, {"stake": 3}]
    nodes_set = list_of_dicst_to_set(nodes)

    while True:
        validators = get_validators_for_transaction(nodes, 10)

        assert list_of_dicst_to_set(validators) == nodes_set

        if nodes != validators:
            # Since the order is random, at some point the order will be different
            break

    print(validators)


def test_get_validators_for_transaction_2():
    """
    Tests that random selection should at some point return all nodes
    """

    nodes = [{"stake": 1}, {"stake": 2}, {"stake": 3}]

    nodes_set = list_of_dicst_to_set(nodes)

    accumulated = set()
    while True:
        validators = get_validators_for_transaction(nodes, 2)
        print(validators)
        accumulated.update(list_of_dicst_to_set(validators))

        if accumulated == nodes_set:
            break
