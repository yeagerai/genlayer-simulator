# rpc/transaction_utils.py

from typing import Any
import rlp
import codecs
from eth_account._utils.legacy_transactions import Transaction, vrs_from
from eth_account._utils.signing import hash_of_signed_transaction
from eth_account import Account
from eth_utils import to_checksum_address
from hexbytes import HexBytes
from rlp.sedes import binary


def decode_signed_transaction(raw_tx):
    try:
        txn_bytes = HexBytes(raw_tx)
        tx_type = 0

        tx = Transaction.from_bytes(txn_bytes)
        msg_hash = hash_of_signed_transaction(tx)
        vrs = vrs_from(tx)

        # extracting sender address
        sender = Account._recover_hash(msg_hash, vrs=vrs)
        res = tx.as_dict()
        # adding sender to result and cleaning

        res["from"] = sender
        res["to"] =  to_checksum_address(f"0x{res['to'].hex()}") if res["to"] else None
        res["data"] = res["data"].hex()
        res["type"] = res.get("type", tx_type)

    except Exception as e:
        print("Error decoding transaction", e)
        return None

    return res


def transaction_has_valid_signature(raw_tx: str, decoded_tx: dict) -> bool:
    recovered_address = Account.recover_transaction(raw_tx)
    # Compare the recovered address with the 'from' address in the transaction
    return recovered_address == decoded_tx["from"]


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
        "contract_code": decode_data_field(data_decoded["contract_code"]),
        "constructor_args": decode_data_field(data_decoded["constructor_args"]),
    }


class DeploymentContractTransactionPayload(rlp.Serializable):
    fields = [
        ("contract_code", binary),
        ("constructor_args", binary),
    ]


class MethodCallTransactionPayload(rlp.Serializable):
    fields = [("function_name", binary), ("function_args", binary)]
