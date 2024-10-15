from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import call_llm_with_principle


class AsyncInit(IContract):
    async def __init__(self):
        result = await call_llm_with_principle(
            "say 'hello'",
            eq_principle="Any output is acceptable",
        )
        print(result)
        await self.test()
        self.result = result

    async def test(self):
        pass

    def get_result(self) -> str:
        return self.result
