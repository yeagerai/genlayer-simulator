from backend.node.genvm.icontract import IContract
from backend.node.genvm.std.vector_store import VectorStore
from backend.node.genvm.std.models import get_model


# contract class
class VectorStoreTester(IContract):

    # constructor
    def __init__(self):
        model = get_model()
        self.vector_store = VectorStore(model)

    # read methods must start with get_
    def get_closest_vector(self, text: str) -> dict:
        similarity, metadata = self.vector_store.get_closest_vector(text)
        return {"similarity": similarity, "metadata": metadata}

    # write method
    def add_log(self, log: str) -> None:
        self.vector_store.add_text(log, {"log_id": 1})
