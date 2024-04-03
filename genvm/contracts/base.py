import os
import time
import asyncio
import json
import functools

from genvm.contracts.llms import call_ollama

from dotenv import load_dotenv
load_dotenv()

def gas_model_logic():
    return 1

def serialize(obj):
    exclude_attrs = ['mode', 'gas_used', 'non_det_counter', 'non_det_inputs', 'non_det_outputs', 'eq_principles_outs']

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

def icontract(cls):
    class WrappedClass(cls):
        def __init__(self, *args, **kwargs):
            self.mode = ""
            self.gas_used = 0
            self.non_det_counter = 0
            self.non_det_inputs = {}
            self.non_det_outputs = {}
            self.eq_principles_outs = {}
            super(WrappedClass, self).__init__(*args, **kwargs)

        async def call_llm(self, prompt, consensus_eq=None, mode='leader', leader_output=None):
            self.non_det_inputs[self.non_det_counter] = {}
            self.non_det_inputs[self.non_det_counter]["input"] = prompt
            if self.mode == 'leader':
                final_response = await call_ollama("generate", "llama2", prompt, None, None)
                self.non_det_outputs[self.non_det_counter] = {}
                self.non_det_outputs[self.non_det_counter]["output"] = final_response
                self.non_det_counter+=1
                return final_response
            
            elif self.mode == 'validator' and consensus_eq and leader_output:
                validator_response = await call_ollama("generate", "llama2", prompt, None, None)
                self.non_det_outputs[self.non_det_counter] = {}
                self.non_det_outputs[self.non_det_counter]["output"] = validator_response
                eq_prompt = f"Given the equivalence principle '{consensus_eq}', decide whether the following two outputs can be considered equivalent.\nOutput 1: {leader_output}\nOutput 2: {validator_response}\nRespond with: TRUE or FALSE"
                validation_response = await call_ollama("generate", "llama2", eq_prompt, None, None)

                agreement = True if validation_response.strip().upper() == "TRUE" else False
                self.eq_principles_outs[self.non_det_counter] = {}
                self.eq_principles_outs[self.non_det_counter]["reasoning"] = validation_response
                self.eq_principles_outs[self.non_det_counter]["agrees_with_leader"] = agreement
                self.non_det_counter+=1
                return agreement, validator_response

            else:
                raise ValueError("Invalid mode or missing parameters for validator.")

        def _write_receipt(self, method_name, args):
            receipt = {
                "method": method_name,
                "args":args,
                "gas_used": self.gas_used,
                "mode": self.mode,
                "contract_state": serialize(self),
                "non_det_inputs": self.non_det_inputs,
                "non_det_outputs": self.non_det_outputs,
                "eq_principles_outs": self.eq_principles_outs
            }

            with open(os.environ.get('GENVMCONLOC') + '/receipt.json', 'w') as file:
                if int(os.environ.get('DEBUG')) == 1:
                    print('--- START: receipt.json ---')
                    print(receipt)
                    print('--- END: receipt.json ---')
                json.dump(receipt, file)

        def __getattribute__(self, name):
            orig_attr = super().__getattribute__(name)
            if callable(orig_attr) and not name.startswith("_"):
                @functools.wraps(orig_attr)
                async def wrapped_function(*args, **kwargs):
                    self.gas_used = gas_model_logic()

                    if asyncio.iscoroutinefunction(orig_attr):
                        output = await orig_attr(*args, **kwargs)
                    else:
                        output = orig_attr(*args, **kwargs)
                    
                    if self.mode == 'leader':
                        self._write_receipt(name, args)
                        print("Leader execution has ended.")
                        time.sleep(5)
                    elif self.mode == 'validator':
                        # Validator logic goes here, using leader's log
                        print("Validator execution has ended.")
                        time.sleep(5)

                    return output
                return wrapped_function
            else:
                return orig_attr
    return WrappedClass
