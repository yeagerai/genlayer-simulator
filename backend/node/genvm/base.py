# backend/node/genvm/base.py

import inspect
import ast
import re
import asyncio
import pickle
import base64
import sys
from contextlib import contextmanager

from backend.database_handler.contract_snapshot import ContractSnapshot
from backend.node.genvm.equivalence_principle import EquivalencePrinciple
from backend.node.genvm.code_enforcement import code_enforcement_check
from backend.node.genvm.std.vector_store import VectorStore


@contextmanager
def safe_globals():
    old_globals = globals().copy()
    globals().update(
        {
            "contract_runner": None,
            "VectorStore": VectorStore,
        }
    )
    try:
        yield
    finally:
        globals().update(old_globals)


class ContractRunner:
    def __init__(self, mode: str, node_config: dict):
        self.mode = mode  # if the node is acting as "validator" or "leader"
        self.node_config = node_config  # provider, model, config, stake
        self.from_address = None  # the address of the transaction sender
        self.gas_used = 0  # the amount of gas used by the contract
        self.eq_num = 0  # keeps track of the eq principle number being executed
        self.eq_outputs = {
            "leader": {}
        }  # the eq principle outputs for the leader and validators


class GenVM:
    eq_principle = EquivalencePrinciple

    def __init__(
        self,
        snapshot: ContractSnapshot,
        validator_mode: str,
        validator_info: dict,
    ):
        self.snapshot = snapshot
        self.validator_mode = validator_mode

        self.contract_runner = ContractRunner(validator_mode, validator_info)

    @staticmethod
    def _get_contract_class_name(contract_code: str) -> str:
        pattern = r"class (\w+)\(IContract\):"
        matches = re.findall(pattern, contract_code)
        if len(matches) == 0:
            raise Exception("No class name found")
        return matches[0]

    def _generate_receipt(self, class_name, encoded_object, method_name, args):
        receipt = {
            # You can't get the name of the inherited class here
            "class": class_name,
            "method": method_name,
            "args": args,
            "gas_used": self.contract_runner.gas_used,
            "mode": self.contract_runner.mode,
            "contract_state": encoded_object,
            "node_config": self.contract_runner.node_config,
            "eq_outputs": self.contract_runner.eq_outputs,
        }

        return receipt

    def deploy_contract(
        self,
        from_address: str,
        code_to_deploy: str,
        constructor_args: dict,
    ):
        class_name = self._get_contract_class_name(code_to_deploy)
        code_enforcement_check(code_to_deploy, class_name)
        self.contract_runner.from_address = from_address

        with safe_globals():
            globals()["contract_runner"] = self.contract_runner
            local_namespace = {}
            exec(code_to_deploy, globals(), local_namespace)

            contract_class = local_namespace[class_name]

            module = sys.modules[__name__]
            setattr(module, class_name, contract_class)

            current_contract = contract_class(**constructor_args)

            pickled_object = pickle.dumps(current_contract)
            encoded_pickled_object = base64.b64encode(pickled_object).decode("utf-8")

            ## Clean up
            delattr(module, class_name)

        return self._generate_receipt(
            class_name, encoded_pickled_object, "__init__", [constructor_args]
        )

    async def run_contract(
        self, from_address: str, function_name: str, args: list, leader_receipt: dict
    ):
        self.contract_runner.from_address = from_address
        contract_code = self.snapshot.contract_code

        with safe_globals():
            globals()["contract_runner"] = self.contract_runner
            local_namespace = {}
            # Execute the code to ensure all classes are defined in the local_namespace
            exec(contract_code, globals(), local_namespace)

            # Ensure the class and other necessary elements are in the global local_namespace if needed
            for name, value in local_namespace.items():
                globals()[name] = value

            self.eq_principle.contract_runner = self.contract_runner

            contract_encoded_state = self.snapshot.encoded_state
            decoded_pickled_object = base64.b64decode(contract_encoded_state)
            current_contract = pickle.loads(decoded_pickled_object)

            if self.contract_runner.mode == "validator":
                leader_receipt_eq_result = leader_receipt["result"]["eq_outputs"][
                    "leader"
                ]
                self.contract_runner.eq_outputs["leader"] = leader_receipt_eq_result

            function_to_run = getattr(current_contract, function_name, None)
            if asyncio.iscoroutinefunction(function_to_run):
                await function_to_run(*args)
            else:
                function_to_run(*args)

            pickled_object = pickle.dumps(current_contract)
            encoded_pickled_object = base64.b64encode(pickled_object).decode("utf-8")
            class_name = self._get_contract_class_name(contract_code)

        return self._generate_receipt(
            class_name, encoded_pickled_object, function_name, [args]
        )

    @staticmethod
    def get_contract_schema(contract_code: str) -> dict:

        namespace = {}
        with safe_globals():
            exec(contract_code, globals(), namespace)
            class_name = GenVM._get_contract_class_name(contract_code)

            iclass = namespace[class_name]

            members = inspect.getmembers(iclass)

            # Find all class methods
            methods = {}
            functions_and_methods = [
                m for m in members if inspect.isfunction(m[1]) or inspect.ismethod(m[1])
            ]
            for name, member in functions_and_methods:
                signature = inspect.signature(member)

                inputs = {}
                for (
                    method_variable_name,
                    method_variable,
                ) in signature.parameters.items():
                    if method_variable_name != "self":
                        annotation = str(method_variable.annotation)[8:-2]
                        inputs[method_variable_name] = str(annotation)

                return_annotation = str(signature.return_annotation)[8:-2]

                if return_annotation == "inspect._empty":
                    return_annotation = "None"

                result = {"inputs": inputs, "output": return_annotation}

                methods[name] = result

            # Find all class variables
            variables = {}
            tree = ast.parse(contract_code)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    for stmt in node.body:
                        if isinstance(stmt, ast.AnnAssign):
                            if hasattr(stmt.annotation, "id") and hasattr(
                                stmt.target, "id"
                            ):
                                variables[stmt.target.id] = stmt.annotation.id

            abi = GenVM.generate_abi_from_schema_methods(methods)

            contract_schema = {
                "class": class_name,
                "methods": methods,
                "variables": variables,
                "abi": abi,
            }

        return contract_schema

    @staticmethod
    def get_abi_param_type(param_type: str) -> str:
        if param_type == "int":
            return "uint256"
        if param_type == "str":
            return "string"
        if param_type == "bool":
            return "bool"
        if param_type == "dict":
            return "bytes"
        if param_type == "list":
            return "bytes"
        if param_type == "None":
            return "None"
        return param_type

    @staticmethod
    def generate_abi_from_schema_methods(contract_schema_methods: dict) -> list:
        abi = []

        for method_name, method_info in contract_schema_methods.items():
            abi_entry = {
                "name": method_name,
                "type": "function",
                "inputs": [],
                "outputs": [],
            }

            for input_name, input_type in method_info["inputs"].items():
                abi_entry["inputs"].append(
                    {"name": input_name, "type": GenVM.get_abi_param_type(input_type)}
                )

            if method_info["output"]:
                abi_entry["outputs"].append(
                    {
                        "name": "",
                        "type": GenVM.get_abi_param_type(method_info["output"]),
                    }
                )

            if method_name == "__init__":
                abi_entry["type"] = "constructor"
                del abi_entry["name"]
                del abi_entry["outputs"]

            abi.append(abi_entry)

        return abi

    @staticmethod
    def get_contract_data(
        code: str, state: str, method_name: str, method_args: list
    ) -> dict:
        namespace = {}
        with safe_globals():
            # Execute the code to ensure all classes are defined in the namespace
            exec(code, globals(), namespace)

            # Ensure the class and other necessary elements are in the global namespace if needed
            for name, value in namespace.items():
                globals()[name] = value

            decoded_pickled_object = base64.b64decode(state)
            contract_state = pickle.loads(decoded_pickled_object)

            method_to_call = getattr(contract_state, method_name)
            result = method_to_call(*method_args)

            # Clean up
            for name in namespace.keys():
                del globals()[name]

        return result
