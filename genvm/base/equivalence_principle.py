import json
from typing import Optional
import inspect
from genvm.base.context_wrapper import enforce_with_context
from genvm.base import llms
from genvm.base.contract_runner import ContractRunner
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
    contract_runner: ContractRunner

    def __init__(
        self,
        result: dict,
        principle: Optional[str],
        comparative: bool = True,
    ):
        if result != {}:
            raise Exception("result must be empty")
        self.result = result
        self.principle = principle
        self.comparative = comparative
        self.last_method = None
        self.last_args = []

    async def __aenter__(self):
        # 1. check that block does not modify self with ast, else throw error
        # 2. comparative=False => execute eq_principle without running the block
        # 3. change output with leaders' output if agree
        #    skip the block

        caller_method_name = inspect.currentframe().f_back.f_code.co_name
        if caller_method_name == "call_llm_with_principle":
            return self

        caller_frame = inspect.currentframe().f_back
        code_in_eq_bloc = get_code_in_eq_block(caller_frame)
        for code in code_in_eq_bloc:
            if 'self.' in code:
                raise Exception('You cannot modify self inside an equivalence block')

        return self

    async def __aexit__(self):

        caller_frame = inspect.currentframe().f_back
        locals_in_caller = caller_frame.f_locals
        clear_locals(locals_in_caller)

        # check eq principle
        if self.principle == None:
            return

        if self.contract_runner.mode == "validator" and self.comparative == True:
            llm_function = self.__get_llm_function()
            eq_prompt = f"""Given the equivalence principle '{self.principle}', 
            decide whether the following two outputs can be considered equivalent.
            
            Leader's Output: {self.contract_runner.eq_outputs['leader'][str(self.contract_runner.eq_num - 1)]}
            
            Validator's Output: {self.result['validator_value']}
            
            Respond with: TRUE or FALSE"""
            validation_response = await llm_function(
                self.contract_runner.node_config, eq_prompt, None, None
            )
            # if TRUE => nothing, FALSE => fuera todo y un state de disagree

    async def get_webpage(self, url: str):
        url_body = get_webpage_content(url)
        final_response = url_body["response"]
        return final_response

    async def call_llm(self, prompt: str):
        llm_function = self.__get_llm_function()
        final_response = await llm_function(
            self.contract_runner.node_config, prompt, None, None
        )
        return final_response

    def set(self, value):
        if self.contract_runner.mode == "leader":
            self.result["output"] = jsonify(value)
            self.contract_runner.eq_outputs["leader"][
                self.contract_runner.eq_num
            ] = value
        else:
            leaders_output = self.contract_runner.eq_outputs["leader"][
                str(self.contract_runner.eq_num)
            ]
            self.result["validator_value"] = jsonify(value)
            self.result["output"] = jsonify(leaders_output)
        self.contract_runner.eq_num += 1

    def __get_llm_function(self):
        function_name = "call_" + self.contract_runner.node_config["provider"]
        llm_function = getattr(llms, function_name)
        return llm_function


async def call_llm_with_principle(prompt, eq_principle, comparative=True):
    final_result = {}
    async with EquivalencePrinciple(
        result=final_result,
        principle=eq_principle,
        comparative=comparative,
    ) as eq:
        result = await eq.call_llm(prompt)
        eq.set(result)

    return final_result["output"]


async def get_webpage_with_principle(url, eq_principle, comparative=True):
    final_result = {}
    async with EquivalencePrinciple(
        result=final_result,
        principle=eq_principle,
        comparative=comparative,
    ) as eq:
        result = await eq.get_webpage(url)
        eq.set(result)


def jsonify(input_string:str) -> str:
    try:
        return json.loads(input_string)
    except Exception:
        raise Exception("The response from the llm was not valid JSON")

def get_code_in_eq_block(caller_frame):
    caller_source_lines, start_line_number = inspect.getsourcelines(caller_frame)
    line_number = start_line_number
    eq_started = False
    eq_finished = False
    eq_indent = None
    code_in_eq_bloc = []

    for line in caller_source_lines:
        # Get the indent of the eq block
        if line_number == caller_frame.f_lineno:
            eq_indent = line_indent_count(line) + 4
        # Start from the eq block
        if line_number >= caller_frame.f_lineno:
            # Only get thge lines in the eq block
            if eq_started and not eq_finished:
                if eq_indent == line_indent_count(line):
                    code_in_eq_bloc.append(line)
                else:
                    eq_finished = True
            if ' as eq:' in line:
                eq_started = True
        line_number += 1

    return code_in_eq_bloc

def line_indent_count(line:str) -> int:
    return len(line) - len(line.lstrip())

