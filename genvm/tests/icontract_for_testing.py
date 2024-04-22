import inspect
import asyncio
import traceback
from contracts.equivalence_principle import EquivalencePrinciple
from contracts.base import icontract


def iContract_stub(cls):

    class WrappedClass(cls):

        def __init__(self, *args, **kwargs):
            super(WrappedClass, self).__init__(*args, **kwargs)
            #del self.__class__.__getattribute__

        async def _get_webpage(self, url:str, equivalence_criteria:str = None):
            # To ensure the method is not called directly
            stack_trace = traceback.extract_stack()
            corectly_called = False
            if stack_trace[-2].name in ['get_webpage', '__aexit__']:
                corectly_called = True
            if not corectly_called:
                raise Exception('This method can not be called directly. Call it from within an EquivalencePrinciple with block')
            await asyncio.sleep(1)
            return 'icontract._get_webpage('+str(equivalence_criteria)+')'


        async def _call_llm(self, prompt:str, consensus_eq:str=None):
            # To ensure the method is not called directly
            stack_trace = traceback.extract_stack()
            corectly_called = False
            if stack_trace[-2].name in ['call_llm', '__aexit__']:
                corectly_called = True
            if not corectly_called:
                raise Exception('This method can not be called directly. Call it from within an EquivalencePrinciple with block')
            await asyncio.sleep(1)
            return 'icontract._call_llm('+str(consensus_eq)+')'

    return WrappedClass


@iContract_stub
class TestContract:

    def get_test_attributes(self):
        return 'https://python.org/', \
            'simple prompt', \
            'simple eq principle', \
            'simple consensus eq', \
            'simple principle'


    def unittest_method_self_get_webpage(self):
        url, prompt, eq_principle, _, _ = self.get_test_attributes()
        self.get_webpage(url, prompt, eq_principle)

    def unittest_method_self_call_llm(self):
        _, prompt, _, consensus_eq, _ = self.get_test_attributes()
        self.call_llm(prompt, consensus_eq)



    def unittest_method_eq_principle_get_webpage(self):
        url, prompt, eq_principle, _, principle = self.get_test_attributes()
        eq_principle = EquivalencePrinciple(self, principle)
        eq_principle.get_webpage(url, prompt, eq_principle)

    def unittest_method_eq_principle_call_llm(self):
        _, prompt, _, consensus_eq, principle = self.get_test_attributes()
        eq_principle = EquivalencePrinciple(self, principle)
        eq_principle.call_llm(prompt, consensus_eq)



    async def unittest_method_self__get_webpage(self):
        url, _, _, _, principle = self.get_test_attributes()
        return await self._get_webpage(url, principle)

    async def unittest_method_self__call_llm(self):
        _, prompt, _, _, principle = self.get_test_attributes()
        return await self._call_llm(prompt, principle)



    async def unittest_method_with_eq_principle_get_webpage(self):
        url, _, _, _, principle = self.get_test_attributes()
        async with EquivalencePrinciple(self, principle) as eq:
            return await eq.get_webpage(url)

    async def unittest_method_with_eq_principle_call_llm(self):
        _, prompt, _, _, principle = self.get_test_attributes()
        async with EquivalencePrinciple(self, principle) as eq:
            return await eq.call_llm(prompt)



    async def unittest_method_with_eq_principle_self__get_webpage(self):
        url, _, _, _, principle = self.get_test_attributes()
        async with EquivalencePrinciple(self, principle) as eq:
            return await self._get_webpage(url)

    async def unittest_method_with_eq_principle_self__call_llm(self):
        _, prompt, _, _, principle = self.get_test_attributes()
        async with EquivalencePrinciple(self, principle) as eq:
            return await self._call_llm(prompt)



    async def unittest_method_with_eq_principle_self__get_webpage_with_principle(self):
        url, _, _, _, principle = self.get_test_attributes()
        async with EquivalencePrinciple(self, principle) as eq:
            return await self._get_webpage(url, principle)

    async def unittest_method_with_eq_principle_self__call_llm_with_principle(self):
        _, prompt, _, _, principle = self.get_test_attributes()
        async with EquivalencePrinciple(self, principle) as eq:
            return await self._call_llm(prompt, principle)
