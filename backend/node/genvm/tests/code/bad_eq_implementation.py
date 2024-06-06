from genvm.base.equivalence_principle import EquivalencePrinciple


class A:
    async def method1(self):
        final_result = {}
        async with EquivalencePrinciple(
            result=final_result,
            principle="The result['give_coin'] has to be exactly the same",
        ) as eq:
            eq.call_llm("something")
            eq.set(result)
        a = EquivalencePrinciple({"a": 1, "b": 2})
        return final_result["output"]
