import pytest

from icontract_for_testing import TestContract

from dotenv import load_dotenv
load_dotenv()


## Test Eq Principle ###


def test_call_function_in_icontract_that_doesnt_exist():
    test_contract = TestContract()
    try:
        test_contract.this_method_does_not_exist()
    except AttributeError as ae:
        assert str(ae) == "'WrappedClass' object has no attribute 'this_method_does_not_exist'"

def test_self_get_webpage():
    test_contract = TestContract()
    try:
        test_contract.unittest_method_self_get_webpage()
    except AttributeError as ae:
        assert str(ae) == "'WrappedClass' object has no attribute 'get_webpage'"

def test_self_call_llm():
    test_contract = TestContract()
    try:
        test_contract.unittest_method_self_call_llm()
    except AttributeError as ae:
        assert str(ae) == "'WrappedClass' object has no attribute 'call_llm'"

def test_eq_principle_get_webpage():
    test_contract = TestContract()
    try:
        test_contract.unittest_method_eq_principle_get_webpage()
    except RuntimeError as runerr:
        assert str(runerr) == "Methods of EquivalencePrinciple must be called inside a 'with' block."

def test_eq_principle_call_llm():
    test_contract = TestContract()
    try:
        test_contract.unittest_method_eq_principle_call_llm()
    except RuntimeError as runerr:
        assert str(runerr) == "Methods of EquivalencePrinciple must be called inside a 'with' block."


## Test iContract Methods (SUCCESS!) ###


@pytest.mark.asyncio
async def test_with_eq_principle_calls_icontract__get_webpage():
    test_contract = TestContract()
    result = await test_contract.unittest_method_with_eq_principle_get_webpage()
    assert result == "icontract._get_webpage(simple principle)"

@pytest.mark.asyncio
async def test_with_eq_principle_calls_icontract__call_llm():
    test_contract = TestContract()
    try:
        result = await test_contract.unittest_method_with_eq_principle_call_llm()
        assert result == "icontract._call_llm(simple principle)"
    except Exception as e:
        raise e


## Test iContract Methods (FAILED!) ###


@pytest.mark.asyncio
async def test_with_eq_principle_calls_icontract__get_webpage_directly():
    test_contract = TestContract()
    try:
        await test_contract.unittest_method_with_eq_principle_self__get_webpage()
    except Exception as e:
        assert str(e) == 'This method can not be called directly. Call it from within an EquivalencePrinciple with block'

@pytest.mark.asyncio
async def test_with_eq_principle_calls_icontract__call_llm_directly():
    test_contract = TestContract()
    try:
        await test_contract.unittest_method_with_eq_principle_self__call_llm()
    except Exception as e:
        assert str(e) == 'This method can not be called directly. Call it from within an EquivalencePrinciple with block'

@pytest.mark.asyncio
async def test_with_eq_principle_calls_icontract__get_webpage_directly_with_principle():
    test_contract = TestContract()
    try:
        await test_contract.unittest_method_with_eq_principle_self__get_webpage_with_principle()
    except Exception as e:
        assert str(e) == 'This method can not be called directly. Call it from within an EquivalencePrinciple with block'

@pytest.mark.asyncio
async def test_with_eq_principle_calls_icontract__call_llm_directly_with_principle():
    test_contract = TestContract()
    try:
        await test_contract.unittest_method_with_eq_principle_self__call_llm_with_principle()
    except Exception as e:
        assert str(e) == 'This method can not be called directly. Call it from within an EquivalencePrinciple with block'

# TODO: Test that only the last _call_llm or _get_webpage is called.
