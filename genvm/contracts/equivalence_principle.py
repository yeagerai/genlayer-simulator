import inspect
from contracts.context_wrapper import enforce_with_context


def clear_locals(scope):
    inside_eq = False
    local_vars = scope.copy()
    for var in local_vars:
        if inside_eq:
            del scope[var]
        if var == 'eq':
            inside_eq = True

@enforce_with_context
class EquivalencePrinciple:

    def __init__(self, icontract_inst:object, result:dict, principle:str):
        if len(result) > 0:
            raise Exception('result must be empty')
        self.result = result
        self.icontract_inst = icontract_inst
        self.principle = principle
        self.last_method = None
        self.last_args = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.last_method and self.last_args:
            # Check the len(args) match the len(args) of the icontract method
            method_name = getattr(self.icontract_inst, '_'+self.last_method)
            original_args = inspect.getfullargspec(method_name).args
            final_args = self.last_args + [self.principle]
            #if len(final_args) != len(original_args):
            #    raise Exception(str(method_name)+' takes '+str(len(original_args))+' args not '+str(len(final_args))+' args')

            caller_frame = inspect.currentframe().f_back
            locals_in_caller = caller_frame.f_locals
            
            vars = clear_locals(locals_in_caller)

            return await getattr(self.icontract_inst, '_'+self.last_method)(*final_args)

    async def get_webpage(self, url:str):
        self.last_method = inspect.currentframe().f_code.co_name
        self.last_args = [url]
        similarity_test = 'are these two texts 70 percent similar of more'
        return await self.icontract_inst._get_webpage(url, similarity_test)

    async def call_llm(self, prompt:str):
        self.last_method = inspect.currentframe().f_code.co_name
        self.last_args = [prompt]
        try:
            return await self.icontract_inst._call_llm(prompt, self.principle)
        except Exception as e:
            raise Exception('something simple')

    def set(self, value):
        self.result['output'] = value