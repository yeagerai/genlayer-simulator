from backend.database_handler.db_client import DBClient


class ChainSnapshot:
    def __init__(self, dbclient: DBClient): ...


class ContractSnapshot:
    def __init__(self, contract_address: str, dbclient: DBClient):
        self.contract_address = contract_address
        ...
