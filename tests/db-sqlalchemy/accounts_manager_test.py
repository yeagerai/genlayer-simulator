from datetime import datetime
import time
from typing import Iterable

import pytest
from backend.database_handler.accounts_manager import AccountsManager
from backend.database_handler.transactions_processor import TransactionsProcessor
from sqlalchemy.orm import Session


@pytest.fixture
def accounts_manager(
    session: Session, transactions_processor: TransactionsProcessor
) -> Iterable[TransactionsProcessor]:
    yield AccountsManager(session, transactions_processor)


def test_accounts_manager(accounts_manager: AccountsManager):
    address = "0x9F0e84243496AcFB3Cd99D02eA59673c05901501"
    balance = 100
    accounts_manager.fund_account(address, balance)

    account_data = accounts_manager.get_account_or_fail(address)

    assert account_data["id"] == address
    assert account_data["data"]["balance"] == balance
    first_updated_at = account_data["updated_at"]
    assert datetime.fromisoformat(first_updated_at)

    time.sleep(0.1)
    extra_balance = 50
    accounts_manager.fund_account(address, extra_balance)

    account_data = accounts_manager.get_account_or_fail(address)

    assert account_data["id"] == address
    assert account_data["data"]["balance"] == balance + extra_balance
    second_updated_at = account_data["updated_at"]
    assert datetime.fromisoformat(second_updated_at)
    assert first_updated_at < second_updated_at
