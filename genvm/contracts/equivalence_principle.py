from typing import Optional
import inspect
from contracts.context_wrapper import enforce_with_context
from genvm.contracts import llms
from genvm.utils import get_webpage_content


def clear_locals(scope):
    inside_eq = False
    local_vars = scope.copy()
    for var in local_vars:
        if inside_eq:
            del scope[var]
        if var == "eq":
            inside_eq = True


# check that block does not modify self helper


@enforce_with_context
class EquivalencePrinciple:

    def __init__(
        self,
        icontract_inst: object,
        result: dict,
        principle: Optional[str],
        comparative: bool = True,
    ):
        if result != {}:
            raise Exception("result must be empty")
        self.result = result
        self.icontract_inst = icontract_inst
        self.principle = principle
        self.comparative = comparative
        self.last_method = None
        self.last_args = []

    async def __aenter__(self):
        # check that block does not modify self with ast, else throw error
        # comparative=False => execute eq_principle without running the block
        # change output with leaders' output if agree
        # skip the block
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):

        caller_frame = inspect.currentframe().f_back
        locals_in_caller = caller_frame.f_locals
        clear_locals(locals_in_caller)

        # check eq principle
        if self.principle == None:
            return

        if self.icontract_inst.mode == "validator" and self.comparative == True:
            llm_function = self.__get_llm_function()
            eq_prompt = f"""Given the equivalence principle '{self.principle}', 
            decide whether the following two outputs can be considered equivalent.
            
            Leader's Output: {self.icontract_inst.eq_outputs['leader'][str(self.icontract_inst.eq_num - 1)]}
            
            Validator's Output: {self.result['validator_value']}
            
            Respond with: TRUE or FALSE"""
            validation_response = await llm_function(
                self.icontract_inst.node_config, eq_prompt, None, None
            )
            # if TRUE => nothing, FALSE => fuera todo y un state de disagree

    async def get_webpage(self, url: str):
        url_body = get_webpage_content(url)
        final_response = url_body["response"]
        return final_response

    async def call_llm(self, prompt: str):
        llm_function = self.__get_llm_function()
        final_response = await llm_function(
            self.icontract_inst.node_config, prompt, None, None
        )
        return final_response

    def set(self, value):
        if self.icontract_inst.mode == "leader":
            self.result["output"] = value
            self.icontract_inst.eq_outputs["leader"][self.icontract_inst.eq_num] = value
        else:
            self.result["validator_value"] = value
            self.result["output"] = self.icontract_inst.eq_outputs["leader"][
                str(self.icontract_inst.eq_num)
            ]
        self.icontract_inst.eq_num += 1

    def __get_llm_function(self):
        function_name = "call_" + self.icontract_inst.node_config["provider"]
        llm_function = getattr(llms, function_name)
        return llm_function


async def call_llm_with_principle(icontract_inst, prompt, eq_principle, comparative):
    final_result = {}
    async with EquivalencePrinciple(
        icontract_inst=icontract_inst,
        result=final_result,
        principle=eq_principle,
        comparative=comparative,
    ) as eq:
        result = await eq.call_llm(prompt)
        eq.set(result)

    return final_result["output"]


async def get_webpage_with_principle(icontract_inst, url, eq_principle, comparative):
    final_result = {}
    async with EquivalencePrinciple(
        icontract_inst=icontract_inst,
        result=final_result,
        principle=eq_principle,
        comparative=comparative,
    ) as eq:
        result = await eq.get_webpage(url)
        eq.set(result)

    return final_result["output"]
