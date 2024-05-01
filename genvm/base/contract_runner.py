import os
import json
import base64
from dotenv import load_dotenv

load_dotenv()


def gas_model_logic():
    return 1


class ContractRunner:
    def __init__(self):
        self.node_config = json.load(
            open(os.environ.get("GENVMCONLOC") + "/node-config.json")
        )
        self.mode = None
        self.gas_used = 0
        self.eq_num = 0
        self.eq_outputs = {}
        self.eq_outputs["leader"] = {}

    def _set_mode(self, mode: str):
        self.mode = mode

    def _load_leader_eq_outputs(self):
        with open(os.environ.get("GENVMCONLOC") + "/receipt_leader.json", "r") as file:
            self.eq_outputs = json.loads(file.read())["result"]["eq_outputs"]

    def _write_receipt(self, contract_state, method_name, args):
        receipt = {
            # You can't get the name of the inherited class here
            "class": self.__class__.__name__,
            "method": method_name,
            "args": args,
            "gas_used": self.gas_used,
            "mode": self.mode,
            "contract_state": contract_state,
            "node_config": self.node_config,
            "eq_outputs": self.eq_outputs,
        }

        with open(
            os.environ.get("GENVMCONLOC") + f"/receipt_{self.mode}.json", "w"
        ) as file:
            json.dump(receipt, file, indent=4)
