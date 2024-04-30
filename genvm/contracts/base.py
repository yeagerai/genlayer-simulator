import os
import json

from dotenv import load_dotenv

load_dotenv()


def gas_model_logic():
    return 1


def serialize(obj):
    exclude_attrs = [
        "mode",
        "gas_used",
        "eq_num",
        "eq_outputs",
        "node_config",
    ]

    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    elif isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        return {
            k: serialize(v)
            for k, v in obj.__dict__.items()
            if not k.startswith("_") and k not in exclude_attrs
        }
    else:
        raise TypeError(f"Type {type(obj)} not serializable")


class IContract:
    def __init__(self):
        self.node_config = json.load(
            open(os.environ.get("GENVMCONLOC") + "/node-config.json")
        )
        self.mode = None
        self.gas_used = 0
        self.eq_num = 0
        self.eq_outputs = {}
        self.eq_outputs["leader"] = {}

    def _load_leader_eq_outputs(self):
        with open(os.environ.get("GENVMCONLOC") + "/receipt_leader.json", "r") as file:
            self.eq_outputs = json.loads(file.read())["result"]["eq_outputs"]

    def _write_receipt(self, method_name, args):
        receipt = {
            # You can't get the name of the inherited class here
            "class": self.__class__.__name__,
            "method": method_name,
            "args": args,
            "gas_used": self.gas_used,
            "mode": self.mode,
            "contract_state": serialize(self),
            "node_config": self.node_config,
            "eq_outputs": self.eq_outputs,
        }

        with open(
            os.environ.get("GENVMCONLOC") + "/receipt.json", "w"
        ) as file:
            json.dump(receipt, file, indent=4)
