# { "Depends": "py-genlayer:test" }

# Always put above line as first in the contract file
# Upon release it will be changed from `:test` to `:<hash>` and library will be frozen forever

# this imports all types into globals and `genlayer.std` as `gl` (will be imported lazily on first access)
from genlayer import *


# use @gl.contract annotation to mark class as a contract. There can be only one contract class
@gl.contract
class Storage:
    # below you must declare all class fields that you are going to use
    # this fields persist between contract calls
    storage_str: str
    storage_int: u256  # NOTE: `int`s are intentionally not supported! in future `bigint` int alias will be introduced

    # all public methods must have type annotations to be user friendly

    # constructor, must not be public
    def __init__(self, initial_str_storage: str):
        self.storage_str = initial_str_storage

    # methods that don't modify anything must be annotated with view
    @gl.public.view
    def get_storage(self) -> str:
        return self.storage_str

    # keyword arguments are supported as well, however, they should not be mixed with positional,
    # in python terms it means that function has following signature (note `/`)
    # def debug(self, x: int, /, *, flag: bool) -> str:
    @gl.public.view
    def debug(self, x: int, *, flag: bool) -> None:
        # you can use prints for debugging (even in write methods and non deterministic blocks)
        # however, stdout doesn't go through consensus and is meant for debug use only
        # it also may be absent in the actual node
        print(f"debug: {self.storage_int}, {x}, {flag}")

    # methods that modify storage must be annotated with write
    @gl.public.write
    def update_storage(self, new_storage: str) -> None:
        self.storage_str = new_storage