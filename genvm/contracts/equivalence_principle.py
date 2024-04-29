from typing import Optional
import inspect
from contracts.context_wrapper import enforce_with_context
from genvm.contracts import llms
from genvm.utils import transaction_files, get_webpage_content


def clear_locals(scope):
    inside_eq = False
    local_vars = scope.copy()
    for var in local_vars:
        if inside_eq:
            del scope[var]
        if var == "eq":
            inside_eq = True


@enforce_with_context
class EquivalencePrinciple:

    def __init__(
        self,
        icontract_inst: object,
        result: dict,
        principle: Optional[str],
        comparative: bool = True,
    ):
        if len(result) > 0:
            raise Exception("result must be empty")
        self.result = result
        self.icontract_inst = icontract_inst
        self.principle = principle
        self.comparative = comparative
        self.last_method = None
        self.last_args = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.last_method and self.last_args:
            # Check the len(args) match the len(args) of the icontract method
            method_name = getattr(self.icontract_inst, "_" + self.last_method)
            original_args = inspect.getfullargspec(method_name).args
            final_args = self.last_args + [self.principle]
            # if len(final_args) != len(original_args):
            #    raise Exception(str(method_name)+' takes '+str(len(original_args))+' args not '+str(len(final_args))+' args')

            caller_frame = inspect.currentframe().f_back
            locals_in_caller = caller_frame.f_locals

            clear_locals(locals_in_caller)

            # check eq principle
            if self.icontract_inst.mode == "validator" and self.comparative == True:
                llm_function = self._get_llm_function()
                eq_prompt = f"""Given the equivalence principle '{self.principle}', 
                decide whether the following two outputs can be considered equivalent.
                
                Leader's Output: {self.icontract_inst.non_det_outputs[self.icontract_inst.eqs_num]}
                
                Validator's Output: {self.result['output']}
                
                Respond with: TRUE or FALSE"""
                validation_response = await llm_function(
                    self.node_config, eq_prompt, None, None
                )
                # if TRUE => nothing, FALSE => fuera todo y un state de disagree

            return await getattr(self.icontract_inst, "_" + self.last_method)(
                *final_args
            )

    async def get_webpage(self, url: str):
        url_body = get_webpage_content(url)
        final_response = url_body["response"]
        return final_response

    async def call_llm(self, prompt: str):
        llm_function = self._get_llm_function()
        final_response = await llm_function(
            self.icontract_inst.node_config, prompt, None, None
        )
        return final_response

    def set(self, value):
        if self.icontract_inst.mode == "leader":
            self.result["output"] = value
            self.icontract_inst.non_det_outputs["leader"] = {}
            self.icontract_inst.non_det_outputs["leader"][
                self.icontract_inst.eqs_num
            ] = value
        else:
            self.result["output"] = self.icontract_inst.non_det_outputs["leader"][
                self.icontract_inst.eqs_num
            ]
        self.icontract_inst.eqs_num += 1

    def _get_llm_function(self):
        llm_function = getattr(llms, "call_ollama")
        if self.icontract_inst.node_config["provider"] == "openai":
            llm_function = getattr(llms, "call_openai")
        return llm_function
