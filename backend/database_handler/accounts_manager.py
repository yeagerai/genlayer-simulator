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

    def create_new_account(self, balance: int = 0) -> Account:
        """
        Used when generating intelligent contract's accounts or sending funds to a new account.
        Users should create their accounts client-side
        """
        account = Account.create()
        self._create_new_account_with_address(account.address, balance)
        return account

    def _create_new_account_with_address(self, address: str, balance: int = 0):
        if not self.is_valid_address(address):
            raise ValueError(f"Invalid address: {address}")
        account_state = CurrentState(
            id=address,
            data={"balance": balance},
        )
        self.session.add(account_state)
        self.session.commit()

    def is_valid_address(self, address: str) -> bool:
        return is_valid_address(address)

    def _get_account(self, account_address: str) -> CurrentState | None:
        """Private method to retrieve an account from the data base"""
        account = (
            self.session.query(CurrentState)
            .filter(CurrentState.id == account_address)
            .one_or_none()
        )
        return account

    def get_account_or_fail(self, account_address: str) -> dict:
        """Private method to check if an account exists, and raise an error if not."""
        account_data = self._get_account(account_address)
        if not account_data:
            raise AccountNotFoundError(
                account_address, f"Account {account_address} does not exist."
            )
        return self._parse_account_data(account_data)

    def fund_account(self, account_address: str, amount: int):
        # account creation or balance update
        account = self._get_account(account_address)
        if account is not None:
            # Account exists, update it
            # Dicts are mutable objects, we need to do something in order for SQLAlchemy to track their changes https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html
            # In this case we are copying the dict, updating it and assigning it back to the object, which will trigger the change tracking
            # I (Agustín Díaz) like this approach better than using `MutableDict` because it's more explicit than using the MutableDict class, and also doesn't leak the object to the rest of the code (which can be dangerous given that it's mutable)
            new_data = account.data.copy()
            new_data["balance"] += amount
            account.data = new_data
            self.session.commit()
            print(account)
        else:
            # Account doesn't exist, create it
            self._create_new_account_with_address(account_address, amount)

        # Record transaction
        transaction_data = {
            "from_address": None,
            "to_address": account_address,
            "data": {"action": "fund_account", "amount": amount},
            "value": amount,
            "type": 0,
        }
        self.transactions_processor.insert_transaction(**transaction_data)
