import re
from backend.database_handler.contract_snapshot import ContractSnapshot
from backend.node.genvm.base import GenVM


# Intelligent Contract Execution Log ===> Traceback (most recent call last): File "/app/backend/node/genvm/base.py", line 236, in run_contract function_to_run(*args) File "<string>", line 17, in token_balances File "/app/backend/node/genvm/contract.py", line 28, in __init__ contract_runner.contract_snapshot_factory(address) ^^^^^^^^^^^^^^^ NameError: name 'contract_runner' is not defined
class ContractMeta(type):
    def __getattr__(cls, name):
        def method(*args, **kwargs):
            if not re.match("get_", name):
                raise Exception("Method name must start with 'get_'")

            return GenVM.get_contract_data(
                cls.contract_snapshot.contract_code,
                cls.contract_snapshot.encoded_state,
                name,
                args,
            )

        return method


class Contract(metaclass=ContractMeta):
    def __init__(self, address: str):
        self.address = address

        # global contract_runner
        self.contract_snapshot: ContractSnapshot = (
            contract_runner.contract_snapshot_factory(address)
        )
