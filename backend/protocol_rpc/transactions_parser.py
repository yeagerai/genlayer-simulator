# rpc/transaction_utils.py

import rlp
import codecs
from eth_account._utils.legacy_transactions import Transaction, vrs_from
from eth_account._utils.signing import hash_of_signed_transaction
from eth_account import Account
from eth_utils import to_checksum_address
from hexbytes import HexBytes
from rlp.sedes import binary
from backend.protocol_rpc.types import (
    DecodedTransaction,
    DecodedMethodCallData,
    DecodedDeploymentData,
)


def decode_signed_transaction(raw_transaction) -> DecodedTransaction:
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
            sender,
            to_address,
            data,
            signed_transaction_as_dict.get("type", 0),
            value,
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


def decode_data_field(input: HexBytes) -> str:
    param = input.hex().replace("0x", "")
    return codecs.decode(param, "hex").decode("utf-8")


def decode_method_call_data(data: str) -> DecodedMethodCallData:
    data_bytes = HexBytes(data)
    data_decoded = rlp.decode(data_bytes, MethodCallTransactionPayload)

    return DecodedMethodCallData(
        decode_data_field(data_decoded["function_name"]),
        decode_data_field(data_decoded["function_args"]),
    )


def decode_deployment_data(data: str) -> DecodedDeploymentData:
    data_bytes = HexBytes(data)
    data_decoded = rlp.decode(data_bytes, DeploymentContractTransactionPayload)

    return DecodedDeploymentData(
        decode_data_field(data_decoded["contract_code"]),
        decode_data_field(data_decoded["constructor_args"]),
    )


class DeploymentContractTransactionPayload(rlp.Serializable):
    fields = [
        ("contract_code", binary),
        ("constructor_args", binary),
    ]


class MethodCallTransactionPayload(rlp.Serializable):
    fields = [("function_name", binary), ("function_args", binary)]
