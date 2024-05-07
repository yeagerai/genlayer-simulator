import pytest

from icontract_for_testing import TestContract

from dotenv import load_dotenv
load_dotenv()

initial_value = "something"


# TODO: This
@pytest.mark.asyncio
async def test_function_get_webpage_with_principle():
    test_contract = TestContract(initial_value)
    result = await test_contract.unittest_method_self_get_webpage()
    assert 'python' in result

