from typing import Optional

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    Enum,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass
import datetime
import decimal
import enum


class TransactionStatus(enum.Enum):
    PENDING = "PENDING"
    CANCELED = "CANCELED"
    PROPOSING = "PROPOSING"
    COMMITTING = "COMMITTING"
    REVEALING = "REVEALING"
    ACCEPTED = "ACCEPTED"
    FINALIZED = "FINALIZED"
    UNDETERMINED = "UNDETERMINED"


# We map them to `DataClass`es in order to have better type hints https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#declarative-dataclass-mapping
class Base(MappedAsDataclass, DeclarativeBase):
    pass


class CurrentState(Base):
    __tablename__ = "current_state"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="current_state_pkey"),
        CheckConstraint("balance >= 0", name="check_balance_non_negative"),
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    data: Mapped[dict] = mapped_column(JSONB)
    balance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True),
        init=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )


class Transactions(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("type = ANY (ARRAY[0, 1, 2])", name="transactions_type_check"),
        PrimaryKeyConstraint("id", name="transactions_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(
            TransactionStatus,
            name="transaction_status",
        ),
        server_default=text("'PENDING'::transaction_status"),
        nullable=False,
    )
    from_address: Mapped[Optional[str]] = mapped_column(String(255))
    to_address: Mapped[Optional[str]] = mapped_column(String(255))
    input_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    data: Mapped[Optional[dict]] = mapped_column(JSONB)
    consensus_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    nonce: Mapped[Optional[int]] = mapped_column(Integer)
    value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    type: Mapped[Optional[int]] = mapped_column(Integer)
    gaslimit: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=func.current_timestamp(), init=False
    )
    r: Mapped[Optional[int]] = mapped_column(Integer)
    s: Mapped[Optional[int]] = mapped_column(Integer)
    v: Mapped[Optional[int]] = mapped_column(Integer)


class TransactionsAudit(Base):
    __tablename__ = "transactions_audit"
    __table_args__ = (PrimaryKeyConstraint("id", name="transactions_audit_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    transaction_id: Mapped[Optional[int]] = mapped_column(Integer)
    data: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=func.current_timestamp(), init=False
    )


class Validators(Base):
    __tablename__ = "validators"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="validators_pkey"),
        CheckConstraint("stake >= 0", name="stake_unsigned_int"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    stake: Mapped[int] = mapped_column(Integer)
    config: Mapped[dict] = mapped_column(JSONB)
    address: Mapped[Optional[str]] = mapped_column(String(255))
    provider: Mapped[Optional[str]] = mapped_column(String(255))
    model: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=func.current_timestamp(), init=False
    )
