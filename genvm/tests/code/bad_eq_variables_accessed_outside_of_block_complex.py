from genvm.base.equivalence_principle import EquivalencePrinciple

class A:

    def __init__(self) -> None:
        pass

    async def method1(self):
        final_result = {}
        async with EquivalencePrinciple(
            result=final_result,
            principle="The result['give_coin'] has to be exactly the same"
        ) as eq:
            result = await eq.call_llm("something")
            name = 'james'
            age = 38
            eq.set(result)
        name = 'dave'
        another_final_result = {}
        async with EquivalencePrinciple(
            result=another_final_result,
            principle="The result['give_coin'] has to be exactly the same"
        ) as eq:
            result = await eq.call_llm("something")
            passing_through = final_result['output']
            location = "Spain"
            eq.set(result)
        age = 58
        location = "France"
        return another_final_result["output"]