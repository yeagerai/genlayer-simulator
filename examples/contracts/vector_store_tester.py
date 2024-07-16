from backend.node.genvm.icontract import IContract
from backend.node.genvm.std.vector_store import VectorStore


# contract class
class VectorStoreTester(IContract):

    # constructor
    def __init__(self):
        self.vector_store = VectorStore()

    # read methods must start with get_
    def get_closest_vector(self, text: str) -> dict:
        return self.vector_store.get_closest_vector(text)

    # write method
    def add_log(self, log: str) -> None:
        self.vector_store.add_text(log, {"log_id": 1})
