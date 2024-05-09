from genvm.base.equivalence_principle import (
    EquivalencePrinciple,
    call_llm_with_principle,
    get_webpage_with_principle
)


class TestContract:

    def get_test_attributes(self):
        return (
            "https://python.org/",
            "Say the word 'hello'",
            "both pieces of text should have 'python' in them",
            "both pieces of text should have 'hello' in them",
            "the results have to be eighty percent similar",
        )

    def __init__(self, initial_value):
        self.initial_value = initial_value


    async def unittest_method_self_get_webpage(self):
        url, prompt, eq_principle, _, _ = self.get_test_attributes()
        return await get_webpage_with_principle(url, prompt, eq_principle)

    async def unittest_method_self_call_llm(self):
        _, prompt, _, consensus_eq, _ = self.get_test_attributes()
        return await call_llm_with_principle(prompt, consensus_eq)

    async def unittest_method_with_eq_principle_get_webpage(self):
        final_result = {}
        url, _, _, _, principle = self.get_test_attributes()
        async with EquivalencePrinciple(final_result, principle) as eq:
            result = await eq.get_webpage(url)
            eq.set(result)
        return final_result["output"]

    async def unittest_method_with_eq_principle_call_llm(self):
        final_result = {}
        _, prompt, _, _, principle = self.get_test_attributes()
        async with EquivalencePrinciple(final_result, principle) as eq:
            result = await eq.call_llm(prompt)
            eq.set(result)
        return final_result["output"]
