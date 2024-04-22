import inspect
from contracts.context_wrapper import enforce_with_context


@enforce_with_context
class EquivalencePrinciple:
    def __init__(self, icontract_inst:object, principle:str):
        self.icontract_inst = icontract_inst
        self.principle = principle
        self.last_method = None
        self.last_args = []

    def __enter__(self):
        return self

    async def __exit__(self, exc_type, exc_value, traceback):
        if self.last_method and self.last_args:
            # Check the len(args) match the len(args) of the icontract method
            method_name = getattr(self.icontract_inst, '_'+self.last_method)
            original_args = inspect.getfullargspec(method_name).args
            final_args = self.last_args + [self.principle]
            if len(final_args) != len(original_args):
                raise Exception(str(method_name)+' takes '+str(len(original_args))+' args not '+str(len(final_args))+' args')

            return await getattr(self.icontract_inst, '_'+self.last_method)(*final_args)

    async def get_webpage(self, url:str):
        self.last_method = inspect.currentframe().f_code.co_name
        self.last_args = [url]
        return await self.icontract_inst._get_webpage(url, self.principle)

    async def call_llm(self, prompt:str):
        self.last_method = inspect.currentframe().f_code.co_name
        self.last_args = [prompt]
        return await self.icontract_inst._call_llm(prompt, self.principle)
