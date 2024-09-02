# database_handler/contract_snapshot.py
from .models import CurrentState
from sqlalchemy.orm import Session


class ContractSnapshot:
    """
    Warning: if you initialize this class with a contract_address:
    - The contract_address must exist in the database.
    - `self.contract_data`, `self.contract_code` and `self.cencoded_state` will be loaded from the database **only once** at initialization.
    """

    def __init__(self, contract_address: str, session: Session):
        self.session = session

        if contract_address is not None:
            self.contract_address = contract_address

            contract_account = self._load_contract_account()
            self.contract_data = contract_account.data
            self.contract_code = self.contract_data["code"]
            self.encoded_state = self.contract_data["state"]

    def _load_contract_account(self) -> CurrentState:
        """Load and return the current state of the contract from the database."""

        return (
            self.session.query(CurrentState)
            .filter(CurrentState.id == self.contract_address)
            .one()
        )

    def register_contract(self, contract: dict):
        """Register a new contract in the database."""
        current_contract = (
            self.session.query(CurrentState).filter_by(id=contract["id"]).one()
        )

        current_contract.data = contract["data"]
        self.session.commit()

    def update_contract_state(self, new_state: str):
        """Update the state of the contract in the database."""
        new_contract_nada = {
            "code": self.contract_data["code"],
            "state": new_state,
        }

        contract = (
            self.session.query(CurrentState).filter_by(id=self.contract_address).one()
        )
        contract.data = new_contract_nada
        self.session.commit()
