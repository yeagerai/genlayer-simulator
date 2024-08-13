from backend.node.genvm.icontract import IContract
from backend.node.genvm.std.vector_store import VectorStore


# contract class
class LogIndexer(IContract):

    # constructor
    def __init__(self):
        self.vector_store = VectorStore()

    # read methods must start with get_
    def get_closest_vector(self, text: str) -> dict:
        result = self.vector_store.get_closest_vector(text)
        if result is None:
            return None
        return {
            "similarity": result[0],
            "id": result[1],
            "text": result[2],
            "metadata": result[3],
            "vector": result[4],
        }

    # write method
    def add_log(self, log: str, log_id: int) -> None:
        self.vector_store.add_text(log, {"log_id": log_id})

    def update_log(self, id: int, log: str, log_id: int) -> None:
        self.vector_store.update_text(id, log, {"log_id": log_id})

    def remove_log(self, id: int) -> None:
        self.vector_store.delete_vector(id)

    def get_vector_metadata(self, id: int) -> None:
        _, metadata = self.vector_store.get_vector(id)
        return metadata
