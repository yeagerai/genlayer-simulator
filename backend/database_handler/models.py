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
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
import decimal


class Base(DeclarativeBase):
    pass


class CurrentState(Base):
    __tablename__ = "current_state"
    __table_args__ = (PrimaryKeyConstraint("id", name="current_state_pkey"),)

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    data: Mapped[dict] = mapped_column(JSONB)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )


class Transactions(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("type = ANY (ARRAY[0, 1, 2])", name="transactions_type_check"),
        PrimaryKeyConstraint("id", name="transactions_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[Optional[str]] = mapped_column(
        Enum(
            "PENDING",
            "CANCELED",
            "PROPOSING",
            "COMMITTING",
            "REVEALING",
            "ACCEPTED",
            "FINALIZED",
            "UNDETERMINED",
            name="transaction_status",
        ),
        server_default=text("'PENDING'::transaction_status"),
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
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )
    r: Mapped[Optional[int]] = mapped_column(Integer)
    s: Mapped[Optional[int]] = mapped_column(Integer)
    v: Mapped[Optional[int]] = mapped_column(Integer)


class TransactionsAudit(Base):
    __tablename__ = "transactions_audit"
    __table_args__ = (PrimaryKeyConstraint("id", name="transactions_audit_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_id: Mapped[Optional[int]] = mapped_column(Integer)
    data: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )


class Validators(Base):
    __tablename__ = "validators"
    __table_args__ = (PrimaryKeyConstraint("id", name="validators_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stake: Mapped[decimal.Decimal] = mapped_column(Numeric)
    config: Mapped[dict] = mapped_column(JSONB)
    address: Mapped[Optional[str]] = mapped_column(String(255))
    provider: Mapped[Optional[str]] = mapped_column(String(255))
    model: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )
