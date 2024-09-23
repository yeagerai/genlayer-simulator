import pytest
from backend.protocol_rpc.transactions_parser import (
    decode_method_call_data,
    DecodedMethodCallData,
    decode_deployment_data,
    DecodedDeploymentData,
)
from rlp import encode


@pytest.mark.parametrize(
    "data, expected_result",
    [
        (
            encode(["class Test(name: str)", '{ "name": "John Doe" }', False]),
            DecodedMethodCallData(
                function_name="class Test(name: str)",
                function_args='{ "name": "John Doe" }',
                leader_only=False,
            ),
        ),
        (
            encode(["class Test(name: str)", '{ "name": "John Doe" }', True]),
            DecodedMethodCallData(
                function_name="class Test(name: str)",
                function_args='{ "name": "John Doe" }',
                leader_only=True,
            ),
        ),
        (
            encode(
                ["class Test(name: str)", '{ "name": "John Doe" }']
            ),  # Should fallback to default
            DecodedMethodCallData(
                function_name="class Test(name: str)",
                function_args='{ "name": "John Doe" }',
                leader_only=False,
            ),
        ),
    ],
)
def test_decode_method_call_data(data, expected_result):
    assert decode_method_call_data(data) == expected_result


@pytest.mark.parametrize(
    "data, expected_result",
    [
        (
            encode(["class Test(name: str)", '{ "name": "John Doe" }', False]),
            DecodedDeploymentData(
                contract_code="class Test(name: str)",
                constructor_args='{ "name": "John Doe" }',
                leader_only=False,
            ),
        ),
        (
            encode(["class Test(name: str)", '{ "name": "John Doe" }', True]),
            DecodedDeploymentData(
                contract_code="class Test(name: str)",
                constructor_args='{ "name": "John Doe" }',
                leader_only=True,
            ),
        ),
        (
            encode(["class Test(name: str)", '{ "name": "John Doe" }']),
            DecodedDeploymentData(
                contract_code="class Test(name: str)",
                constructor_args='{ "name": "John Doe" }',
                leader_only=False,
            ),
        ),
    ],
)
def test_decode_deployment_data(data, expected_result):
    assert decode_deployment_data(data) == expected_result
