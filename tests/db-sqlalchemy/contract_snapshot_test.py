from sqlalchemy.orm import Session

from backend.database_handler.contract_snapshot import ContractSnapshot
from backend.database_handler.models import CurrentState


def test_contract_snapshot_with_contract(session: Session):
    # Pre-load contract
    contract_address = "0x123456"
    contract_code = "code"
    contract_state = "state"
    contract = CurrentState(
        id=contract_address, data={"code": contract_code, "state": contract_state}
    )

    session.add(contract)
    session.commit()

    # Test ContractSnapshot
    contract_snapshot = ContractSnapshot(contract_address, lambda: session)

    assert contract_snapshot.contract_address == contract_address
    assert contract_snapshot.contract_data["code"] == contract_code
    assert contract_snapshot.contract_data["state"] == contract_state

    new_state = "new_state"
    contract_snapshot.update_contract_state(new_state)

    actual_contract = session.query(CurrentState).filter_by(id=contract_address).one()

    assert actual_contract.data["state"] == new_state
    assert actual_contract.data["code"] == contract_code


def test_contract_snapshot_without_contract(session: Session):
    contract_snapshot = ContractSnapshot(None, lambda: session)

    assert "contract_address" not in contract_snapshot.__dict__
    assert "contract_data" not in contract_snapshot.__dict__
    assert "contract_code" not in contract_snapshot.__dict__

    contract = {
        "id": "0x123456",
        "data": {"code": "code", "state": "state"},
    }

    contract_snapshot.register_contract(contract)

    actual_contract = session.query(CurrentState).filter_by(id=contract["id"]).one()

    assert actual_contract.data == contract["data"]
    assert actual_contract.id == contract["id"]
    assert actual_contract.data["code"] == contract["data"]["code"]
    assert actual_contract.data["state"] == contract["data"]["state"]