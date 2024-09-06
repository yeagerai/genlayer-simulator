# consensus/services/transactions_db_service.py

from eth_account import Account
from eth_account._utils.validation import is_valid_address

from .models import CurrentState
from backend.database_handler.errors import AccountNotFoundError
from backend.database_handler.transactions_processor import TransactionsProcessor

from sqlalchemy.orm import Session


class AccountsManager:
    def __init__(self, session: Session, transactions_processor: TransactionsProcessor):
        self.session = session
        self.transactions_processor = transactions_processor

    def _parse_account_data(self, account_data: CurrentState) -> dict:
        return {
            "id": account_data.id,
            "data": account_data.data,
            "updated_at": account_data.updated_at.isoformat(),
        }

    def create_new_account(self) -> Account:
        """
        Used when generating intelligent contract's accounts or sending funds to a new account.
        Users should create their accounts client-side
        """
        account = Account.create()
        self.create_new_account_with_address(account.address)
        return account

    def create_new_account_with_address(self, address: str):
        if not self.is_valid_address(address):
            raise ValueError(f"Invalid address: {address}")
        account_state = CurrentState(id=address)
        self.session.add(account_state)
        self.session.commit()

    def is_valid_address(self, address: str) -> bool:
        return is_valid_address(address)

    def get_account(self, account_address: str) -> CurrentState | None:
        """Private method to retrieve an account from the data base"""
        account = (
            self.session.query(CurrentState)
            .filter(CurrentState.id == account_address)
            .one_or_none()
        )
        return account

    def get_account_or_fail(self, account_address: str) -> dict:
        """Private method to check if an account exists, and raise an error if not."""
        account_data = self.get_account(account_address)
        if not account_data:
            raise AccountNotFoundError(
                account_address, f"Account {account_address} does not exist."
            )
        return self._parse_account_data(account_data)

    def get_account_balance(self, account_address: str) -> int:
        account = self.get_account_or_fail(account_address)
        return account.balance

    def is_contract(self, account: dict) -> bool:
        return account.get("data", {}).get("code", False)
