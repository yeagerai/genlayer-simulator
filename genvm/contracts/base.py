import os
import sys
import asyncio
import json
import functools
import inspect
import traceback

from genvm.contracts import llms
from genvm.utils import transaction_files, get_webpage_content

from dotenv import load_dotenv
load_dotenv()

def gas_model_logic():
    return 1

def serialize(obj):
    exclude_attrs = [
        'mode',
        'gas_used',
        'non_det_counter',
        'non_det_inputs',
        'non_det_outputs',
        'eq_principles_outs',
        'node_config'
    ]

    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    elif isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return {k: serialize(v) for k, v in obj.__dict__.items() if not k.startswith('_') and k not in exclude_attrs}
    else:
        raise TypeError(f"Type {type(obj)} not serializable")

# ""something"" => "something"
def clean_response(response):
    return json.dumps(response)[1:-1]


def icontract(cls):
    class WrappedClass(cls):
        def __init__(self, *args, **kwargs):
            self.node_config = json.load(open(os.environ.get('GENVMCONLOC') + '/node-config.json'))
            self.mode = None
            self.gas_used = 0
            self.non_det_counter = 0
            self.non_det_inputs = {}
            self.non_det_outputs = {}
            self.eq_principles_outs = {}
            super(WrappedClass, self).__init__(*args, **kwargs)

        async def _get_webpage(self, url:str, equivalence_criteria:str=None):

            # To ensure the method is not called directly
            if not equivalence_criteria:
                raise Exception('This method can not be called directly. Call it from within an EquivalencePrinciple with block')

            _, _, _, recipt_file = transaction_files()

            llm_function = self.get_llm_function()

            self.non_det_inputs[self.non_det_counter] = {'url': url}

            final_response = None

            if self.node_config['type'] == 'leader':
                self.mode = 'leader'
                stack_trace = traceback.extract_stack()
                if stack_trace[-3].name == '__aexit__':
                    self.non_det_outputs[self.non_det_counter] = '__aexit__ call'
                else:
                    url_body = get_webpage_content(url)
                    self.non_det_outputs[self.non_det_counter] = url_body['response']
                    final_response = url_body['response']
            elif self.node_config['type'] == 'validator':
                self.mode = 'validator'
                # make sure the leader file exists first
                if not os.path.exists(recipt_file):
                    raise Exception(recipt_file + ' does not exist!')
                # get the leader file
                file = open(recipt_file, 'r')
                leader_receipt = json.load(file)
                file.close()
                self.non_det_inputs[self.non_det_counter]['leader_reciept'] = leader_receipt
                # get the webpage
                url_body = get_webpage_content(url)
                self.non_det_outputs[self.non_det_counter] = url_body['response']
                leader_output = leader_receipt['result']['non_det_outputs'][str(self.non_det_counter)]
                # if it's the with's exit function then use the leader's previous output
                if leader_receipt['result']['non_det_outputs'][str(self.non_det_counter)] == '__aexit__ call':
                    leader_output = leader_receipt['result']['non_det_outputs'][str(self.non_det_counter-1)]
                # Compare to the leaders
                eq_prompt = f"Using the following equivalence criteria:\n\nCriteria:\n{equivalence_criteria}\n\nAgainst the follow two blocks of text.\n\nText 1:\n{leader_output}\n\nText 2:\n{url_body['response']}\n\nRespond with True or False"
                similarity_response = await llm_function(self.node_config, eq_prompt, None, None)

                if similarity_response not in ['True', 'False']:
                    raise Exception('Similarity response was not a Boolean ('+similarity_response+')')

                # Store the similarity_response as a boolean
                similar = False
                if similarity_response == 'True':
                    similar = True
                self.eq_principles_outs[self.non_det_counter] = {'is_similar': similar}

                if not similar:
                    # TODO: This needs to be revisted (eq_principle function)
                    # '_call_llm' < 'wrapped_function' <'ask_for_coin' < 'wrapped_function' < 'main' < ...
                    #                                  --------------
                    method_name = inspect.stack()[2].function
                    self._write_receipt(method_name, {})
                    file = open(recipt_file, 'r')
                    validator_recipt = json.load(file)
                    file.close()

                    error_output = {
                        "leader_recipt": leader_receipt,
                        "validator_recipt": validator_recipt,
                        "eq_principle_prompt": clean_response(eq_prompt),
                        "eq_principle_response": similarity_response
                    }
                    with open('/tmp/error.json', 'w') as file:
                        json.dump(error_output, file, indent=4)

                    print('There was limited similarity between the validators output and the leaders output.', file=sys.stderr)
                    sys.exit(1)

                final_response = leader_output
            else:
                raise ValueError("Invalid mode")

            self.non_det_counter+=1

            return final_response


        async def _call_llm(self, prompt:str, consensus_eq:str=None):

            # To ensure the method is not called directly
            if not consensus_eq:
                raise Exception('This method can not be called directly. Call it from within an EquivalencePrinciple with block')

            _, _, _, recipt_file = transaction_files()

            leader_recipt = None
            if self.node_config['type'] == 'validator' and os.path.exists(recipt_file):
                file = open(recipt_file, 'r')
                leader_recipt = json.load(file)
                file.close()

            llm_function = self.get_llm_function()

            self.non_det_inputs[self.non_det_counter] = prompt

            final_response = None

            if self.node_config['type'] == 'leader':
                self.mode = 'leader'
                final_response = await llm_function(self.node_config, prompt, None, None)
                self.non_det_outputs[self.non_det_counter] = final_response
            
            elif self.node_config['type'] == 'validator' and consensus_eq and leader_recipt:
                validator_response = await llm_function(self.node_config, prompt, None, None)
                self.non_det_outputs[self.non_det_counter] = validator_response

                leader_response = leader_recipt['result']['non_det_outputs'][str(self.non_det_counter)]

                eq_prompt = f"Given the equivalence principle '{consensus_eq}', decide whether the following two outputs can be considered equivalent.\nOutput 1: {leader_response}\nOutput 2: {validator_response}\nRespond with: TRUE or FALSE"
                validation_response = await llm_function(self.node_config, eq_prompt, None, None)

                agreement = True if validation_response.strip().upper() == "TRUE" else False
                self.eq_principles_outs[self.non_det_counter] = {
                    "response": validation_response,
                    "agrees_with_leader": agreement
                }
                if not agreement:
                    # 'call_llm' < 'wrapped_function' <'ask_for_coin' < 'wrapped_function' < 'main' < ...
                    #                                  --------------
                    method_name = inspect.stack()[2].function
                    self._write_receipt(method_name, {})
                    file = open(recipt_file, 'r')
                    validator_recipt = json.load(file)
                    file.close()

                    error_output = {
                        "leader_recipt": leader_recipt,
                        "validator_recipt": validator_recipt,
                        "eq_principle_prompt": eq_prompt,
                        "eq_principle_response": validation_response
                    }

                    with open('/tmp/error.json', 'w') as file:
                        json.dump(error_output, file, indent=4)

                    print('The validator did not agree with the leader', file=sys.stderr)

                    sys.exit(1)

                final_response = leader_response

            else:
                raise ValueError("Invalid mode or missing parameters for validator.")
            
            self.non_det_counter+=1
            return final_response

        # This will get excuited under the following TWO conditiions:
        # 1. When the method on the icontract has finished (i.e. ask_for_coin)
        # 2. When a validator disagrees with the leaders outcome
        def _write_receipt(self, method_name, args):
            receipt = {
                # You can't get the name of the inherited class here
                "class": self.__class__.__name__,
                "method": method_name,
                "args":args,
                "gas_used": self.gas_used,
                "mode": self.mode,
                "contract_state": serialize(self),
                "node_config": self.node_config,
                "non_det_inputs": self.non_det_inputs,
                "non_det_outputs": self.non_det_outputs,
                "eq_principles_outs": self.eq_principles_outs
            }

            with open(os.environ.get('GENVMCONLOC') + '/receipt.json', 'w') as file:
                json.dump(receipt, file, indent=4)

        def __getattribute__(self, name):
            new_name = name
            if name == 'get_webpage' or name == 'call_llm':
                new_name = '_' + name
            orig_attr = super().__getattribute__(new_name)
            if new_name == '_get_webpage' or new_name == '_call_llm':
                @functools.wraps(orig_attr)
                async def wrapped_function(*args, **kwargs):
                    self.gas_used = gas_model_logic()

                    if asyncio.iscoroutinefunction(orig_attr):
                        output = await orig_attr(*args, **kwargs)
                    else:
                        output = orig_attr(*args, **kwargs)
                    
                    self._write_receipt(new_name, args)
                    print("Execution Finished!")

                    return output
                return wrapped_function
            else:
                return orig_attr
        

        def get_llm_function(self):
            llm_function = getattr(llms, 'call_ollama')
            if self.node_config['provider'] == 'openai':
                llm_function = getattr(llms, 'call_openai')
            return llm_function

    return WrappedClass
