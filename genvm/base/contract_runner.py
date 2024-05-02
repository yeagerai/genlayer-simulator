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

    def _write_receipt(self, pickled_object, method_name, args):
        encoded_pickled_object = base64.b64encode(pickled_object).decode("utf-8")
        receipt = {
            # You can't get the name of the inherited class here
            "class": self.__class__.__name__,
            "method": method_name,
            "args": args,
            "gas_used": self.gas_used,
            "mode": self.mode,
            "contract_state": encoded_pickled_object,
            "node_config": self.node_config,
            "eq_outputs": self.eq_outputs,
        }

        with open(
            os.environ.get("GENVMCONLOC") + "/receipt.json", "w"
        ) as file:
            json.dump(receipt, file, indent=4)
