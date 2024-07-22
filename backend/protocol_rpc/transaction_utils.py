# rpc/transaction_utils.py

from typing import Any
from enum import Enum
from eth_account._utils.typed_transactions import TypedTransaction
from eth_account._utils.legacy_transactions import Transaction, vrs_from
from eth_account._utils.signing import hash_of_signed_transaction
import rlp
import codecs
from eth_account import Account
from hexbytes import HexBytes
from rlp.sedes import binary


def decode_signed_transaction_and_verify(raw_tx):
    decoded_tx = decode_signed_transaction(raw_tx)

    # Recover the address from the raw tx
    recovered_address = Account.recover_transaction(raw_tx)

    # Compare the recovered address with the 'from' address in the transaction
    if recovered_address == decoded_tx["from"]:
        return decoded_tx
    else:
        return None


def verify_transaction_signature(raw_tx):
    decoded_tx = decode_signed_transaction_and_verify(raw_tx)

    return True if decoded_tx is None else False


def parse_transaction(raw_tx):
    txn_bytes = HexBytes(raw_tx)
    if len(txn_bytes) > 0 and txn_bytes[0] <= 0x7F:
        # We are dealing with a typed transaction.
        tx_type = 2
        tx = TypedTransaction.from_bytes(txn_bytes)
        msg_hash = tx.hash()
        vrs = tx.vrs()
    else:
        # We are dealing with a legacy transaction.
        tx_type = 0

        tx = Transaction.from_bytes(txn_bytes)
        msg_hash = hash_of_signed_transaction(tx)
        vrs = vrs_from(tx)

    return {"tx_type": tx_type, "tx": tx, "msg_hash": msg_hash, "vrs": vrs}


def decode_signed_transaction(raw_tx):
    parsed = parse_transaction(raw_tx)

    tx_type = parsed["tx_type"]
    tx = parsed["tx"]
    msg_hash = parsed["msg_hash"]
    vrs = parsed["vrs"]

    # extracting sender address
    sender = Account._recover_hash(msg_hash, vrs=vrs)
    res = tx.as_dict()
    # adding sender to result and cleaning

    res["from"] = sender
    res["to"] = res["to"].hex()
    res["data"] = res["data"].hex()
    res["type"] = res.get("type", tx_type)

    return res


def decode_data_field(input: HexBytes) -> str:
    param = input.hex().replace("0x", "")
    return codecs.decode(param, "hex").decode("utf-8")


def decode_method_call_data(data: str) -> str:
    data_bytes = HexBytes(data)
    data_decoded = rlp.decode(data_bytes, MethodCallTransactionPayload)
    
    return {
        "function_name": decode_data_field(data_decoded["function_name"]),
        "function_args": decode_data_field(data_decoded["function_args"]),
    }

def decode_deployment_data(data: str) -> str:
    data_bytes = HexBytes(data)
    data_decoded = rlp.decode(data_bytes, DeploymentContractTransactionPayload)

    return {
        "class_name": decode_data_field(data_decoded["class_name"]),
        "contract_code": decode_data_field(data_decoded["contract_code"]),
        "constructor_args": decode_data_field(data_decoded["constructor_args"]),
    }


class DeploymentContractTransactionPayload(rlp.Serializable):
    fields = [
        ("class_name", binary),
        ("contract_code", binary),
        ("constructor_args", binary),
    ]


class MethodCallTransactionPayload(rlp.Serializable):
    fields = [("function_name", binary), ("function_args", binary)]
