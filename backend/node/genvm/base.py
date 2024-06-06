import inspect
import ast
import re
import asyncio
import pickle
import base64
import sys

from backend.database_handler.contract_snapshot import ContractSnapshot
from backend.node.genvm.equivalence_principle import EquivalencePrinciple
from backend.node.genvm.code_enforcement import code_enforcement_check


class GenVM:
    def __init__(
        self,
        snapshot: ContractSnapshot,
        validator_mode,
        node_config,
    ):
        self.snapshot = snapshot
        self.validator_mode = validator_mode
        self.contract_runner = {
            "node_config": node_config,
            "mode": validator_mode,
            "from_address": None,
            "gas_used": 0,
            "eq_num": 0,
            "eq_outputs": {"leader": {}},
        }

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
            "gas_used": self.contract_runner["gas_used"],
            "mode": self.contract_runner["mode"],
            "contract_state": encoded_object,
            "node_config": self.contract_runner["node_config"],
            "eq_outputs": self.contract_runner["eq_outputs"],
        }

        return receipt

    def deploy_contract(self, code_to_deploy, from_address, constructor_args):

        code_enforcement_check(code_to_deploy)
        class_name = self._get_contract_class_name(code_to_deploy)

        self.contract_runner["from_address"] = from_address
        eval(code_to_deploy)
        contract_class = locals()[class_name]  ## en teoria
        current_contract = contract_class(**constructor_args)

        pickled_object = pickle.dumps(current_contract)
        encoded_pickled_object = base64.b64encode(pickled_object).decode("utf-8")
        return self._generate_receipt(
            class_name, encoded_pickled_object, "__init__", [{constructor_args}]
        )

    async def run_contract(self, from_address, function_name, args, leader_receipt):
        self.contract_runner["from_address"] = from_address
        contract_runner = (
            self.contract_runner
        )  # is being used in function_to_run(*args)
        try:
            EquivalencePrinciple.contract_runner = self.contract_runner
        except (ImportError, UnboundLocalError):
            EquivalencePrinciple.contract_runner = self.contract_runner

        contract_encoded_state = self.snapshot.encoded_state
        decoded_pickled_object = base64.b64decode(contract_encoded_state)
        current_contract = pickle.loads(decoded_pickled_object)

        if self.contract_runner["mode"] == "validator":
            self.contract_runner["eq_outputs"]["leader"] = leader_receipt

        class_name = ...
        function_to_run = getattr(current_contract, function_name, None)
        if asyncio.iscoroutinefunction(function_to_run):
            await function_to_run(*args)
        else:
            function_to_run(*args)

        pickled_object = pickle.dumps(current_contract)
        encoded_pickled_object = base64.b64encode(pickled_object).decode("utf-8")
        return self._generate_receipt(
            class_name, encoded_pickled_object, function_name, [args]
        )

    @staticmethod
    def get_contract_schema(contract_code: str) -> dict:

        namespace = {}
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
            for method_variable_name, method_variable in signature.parameters.items():
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

        contract_schema = {
            "class": class_name,
            "methods": methods,
            "variables": variables,
        }

        return contract_schema

    @staticmethod
    def get_contract_data(
        code: str, state: str, method_name: str, method_args: list
    ) -> dict:
        namespace = {}
        exec(code, namespace)

        target_module = sys.modules["__main__"]
        for name, value in namespace.items():
            setattr(target_module, name, value)

        decoded_pickled_object = base64.b64decode(state)
        contract_state = pickle.loads(decoded_pickled_object)
        method_to_call = getattr(contract_state, method_name)
        return method_to_call(*method_args)
