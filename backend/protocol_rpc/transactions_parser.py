# rpc/transaction_utils.py

import rlp
from rlp.sedes import text, boolean
from eth_account import Account
from eth_account._utils.legacy_transactions import Transaction, vrs_from
from eth_account._utils.signing import hash_of_signed_transaction
from eth_utils import to_checksum_address
from hexbytes import HexBytes

from backend.protocol_rpc.types import (
    DecodedDeploymentData,
    DecodedMethodCallData,
    DecodedTransaction,
)


def decode_signed_transaction(raw_transaction: str) -> DecodedTransaction | None:
    try:
        transaction_bytes = HexBytes(raw_transaction)
        signed_transaction = Transaction.from_bytes(transaction_bytes)
        msg_hash = hash_of_signed_transaction(signed_transaction)
        vrs = vrs_from(signed_transaction)

        # extracting sender address
        sender = Account._recover_hash(msg_hash, vrs=vrs)
        signed_transaction_as_dict = signed_transaction.as_dict()
        to_address = (
            to_checksum_address(f"0x{signed_transaction_as_dict['to'].hex()}")
            if signed_transaction_as_dict["to"]
            else None
        )
        value = signed_transaction_as_dict["value"]
        data = (
            signed_transaction_as_dict["data"].hex()
            if signed_transaction_as_dict["data"]
            else None
        )
        return DecodedTransaction(
            from_address=sender,
            to_address=to_address,
            data=data,
            type=signed_transaction_as_dict.get("type", 0),
            value=value,
        )

    except Exception as e:
        print("Error decoding transaction", e)
        return None


def transaction_has_valid_signature(
    raw_transaction: str, decoded_tx: DecodedTransaction
) -> bool:
    recovered_address = Account.recover_transaction(raw_transaction)
    # Compare the recovered address with the 'from' address in the transaction
    return recovered_address == decoded_tx.from_address


def decode_method_call_data(data: str) -> DecodedMethodCallData:
    data_bytes = HexBytes(data)

    try:
        data_decoded = rlp.decode(data_bytes, MethodCallTransactionPayload)
    except rlp.exceptions.DeserializationError as e:
        print("Error decoding method call data, falling back to default:", e)
        data_decoded = rlp.decode(data_bytes, MethodCallTransactionPayloadDefault)

    leader_only = getattr(data_decoded, "leader_only", False)

    return DecodedMethodCallData(
        function_name=data_decoded["function_name"],
        function_args=data_decoded["function_args"],
        leader_only=leader_only,
    )


def decode_deployment_data(data: str) -> DecodedDeploymentData:
    data_bytes = HexBytes(data)

    try:
        data_decoded = rlp.decode(data_bytes, DeploymentContractTransactionPayload)
    except rlp.exceptions.DeserializationError as e:
        print("Error decoding deployment data, falling back to default:", e)
        data_decoded = rlp.decode(
            data_bytes, DeploymentContractTransactionPayloadDefault
        )

    leader_only = getattr(data_decoded, "leader_only", False)

    return DecodedDeploymentData(
        contract_code=data_decoded["contract_code"],
        constructor_args=data_decoded["constructor_args"],
        leader_only=leader_only,
    )


class DeploymentContractTransactionPayload(rlp.Serializable):
    fields = [
        ("contract_code", text),
        ("constructor_args", text),
        ("leader_only", boolean),
    ]


class DeploymentContractTransactionPayloadDefault(rlp.Serializable):
    fields = [
        ("contract_code", text),
        ("constructor_args", text),
    ]


class MethodCallTransactionPayload(rlp.Serializable):
    fields = [
        ("function_name", text),
        ("function_args", text),
        ("leader_only", boolean),
    ]


class MethodCallTransactionPayloadDefault(rlp.Serializable):
    fields = [
        ("function_name", text),
        ("function_args", text),
    ]
