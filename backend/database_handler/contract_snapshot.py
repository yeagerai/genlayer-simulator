# database_handler/contract_snapshot.py
from .models import CurrentState
from sqlalchemy.orm import Session
from typing import Callable

# At this moment, `ContractSnapshot` is creating its own sessions on each method call. This can be further improved by injecting the session into the method. This way, the session can be reused across multiple method calls. This is a common pattern in SQLAlchemy applications.
# Given that it might be a bit verbose to inject the session into each method, there's the possibility of creating a decorator to handle this injection. This decorator would check if the session is already present in the method's keyword arguments. If it's not, it would create a new session and inject it into the method. Here's a possible implementation of this decorator:

# def inject_session(func):
#     """
#     Decorator to inject a session into a function if it's not already present in the function's keyword arguments.
#     It expects to be added to a method of a class that has a `session` attribute.
#     The class is expected to have an `engine` attribute that is an instance of `Engine`.
#     """

#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         # Check if 'session' is in the function's keyword arguments or not
#         if "session" not in kwargs or kwargs["session"] is None:
#             if self.session is not None:
#                 kwargs["session"] = self.session
#                 return func(self, *args, **kwargs)
#             else:
#                 with Session(self.engine) as session:
#                     kwargs["session"] = session
#         return func(*args, **kwargs)
#     return wrapper


class ContractSnapshot:
    """
    Warning: if you initialize this class with a contract_address:
    - The contract_address must exist in the database.
    - `self.contract_data`, `self.contract_code` and `self.cencoded_state` will be loaded from the database **only once** at initialization.
    """

    def __init__(self, contract_address: str, get_session: Callable[[], Session]):
        self.get_session = get_session

        if contract_address is not None:
            self.contract_address = contract_address

            contract_account = self._load_contract_account()
            self.contract_data = contract_account.data
            self.contract_code = self.contract_data["code"]
            self.encoded_state = self.contract_data["state"]

    def _load_contract_account(self) -> CurrentState:
        """Load and return the current state of the contract from the database."""
        with self.get_session() as session:
            return (
                session.query(CurrentState)
                .filter(CurrentState.id == self.contract_address)
                .one()
            )

    def register_contract(self, contract: dict):
        """Register a new contract in the database."""
        with self.get_session() as session:
            current_contract = (
                session.query(CurrentState).filter_by(id=contract["id"]).one()
            )

            current_contract.data = contract["data"]
            session.commit()

    def update_contract_state(self, new_state: str):
        """Update the state of the contract in the database."""
        new_contract_nada = {
            "code": self.contract_data["code"],
            "state": new_state,
        }

        with self.get_session() as session:
            contract = (
                session.query(CurrentState).filter_by(id=self.contract_address).one()
            )
            contract.data = new_contract_nada
            session.commit()
