import os
import asyncio
import json
import functools

from dotenv import load_dotenv

load_dotenv()


def gas_model_logic():
    return 1


def serialize(obj):
    exclude_attrs = [
        "mode",
        "gas_used",
        "non_det_counter",
        "non_det_inputs",
        "non_det_outputs",
        "eq_principles_outs",
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


def icontract(cls):
    class WrappedClass(cls):
        def __init__(self, *args, **kwargs):
            self.node_config = json.load(
                open(os.environ.get("GENVMCONLOC") + "/node-config.json")
            )
            self.mode = None
            self.gas_used = 0
            self.non_det_counter = 0
            self.non_det_inputs = {}
            self.non_det_outputs = {}
            self.eq_principles_outs = {}
            super(WrappedClass, self).__init__(*args, **kwargs)

        # This will get excuited under the following TWO conditiions:
        # 1. When the method on the icontract has finished (i.e. ask_for_coin)
        # 2. When a validator disagrees with the leaders outcome
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
                "non_det_inputs": self.non_det_inputs,
                "non_det_outputs": self.non_det_outputs,
                "eq_principles_outs": self.eq_principles_outs,
            }

            with open(os.environ.get("GENVMCONLOC") + "/receipt.json", "w") as file:
                json.dump(receipt, file, indent=4)

        def __getattribute__(self, name):
            new_name = name

            orig_attr = super().__getattribute__(new_name)

            @functools.wraps(orig_attr)
            async def wrapped_function(*args, **kwargs):
                self.gas_used = gas_model_logic()

                if asyncio.iscoroutinefunction(orig_attr):
                    output = await orig_attr(*args, **kwargs)
                else:
                    output = orig_attr(*args, **kwargs)

                # hardcore comparison
                self._write_receipt(new_name, args)
                print("Execution Finished!")

                return output

            return wrapped_function

    return WrappedClass
