from web3 import Web3
import json
from eth_account import Account

# docker should contain:
# npx hardhat compile
# npx hardhat node

# Connect to Hardhat Network
hardhat_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(hardhat_url))

# Check connection
if not web3.is_connected():
    print("Failed to connect to Hardhat Network")
    exit()


def clean_hex_string(hex_str):
    if isinstance(hex_str, bytes):
        return Web3.to_hex(hex_str)
    return hex_str


def decode_eth_dict(receipt_dict):
    decoded = {}
    for key, value in dict(receipt_dict).items():
        if key == "logs":
            decoded[key] = [decode_log(log) for log in value]
        elif isinstance(value, bytes):
            decoded[key] = Web3.to_hex(value)
        elif isinstance(value, (list, tuple)):
            decoded[key] = [clean_hex_string(item) for item in value]
        else:
            decoded[key] = value
    return decoded


def decode_log(log):
    decoded_log = {}
    for key, value in dict(log).items():
        if key == "data":
            try:
                # Convert to hex first
                hex_data = Web3.to_hex(value)[2:]  # remove '0x' prefix
                # Skip the first 64 chars (32 bytes) which represent the offset
                # and the next 64 chars which represent the length
                message_hex = hex_data[128:]
                # Convert to text and remove null bytes
                decoded_log["data"] = (
                    bytes.fromhex(message_hex).decode("utf-8").rstrip("\x00")
                )
            except Exception as e:
                decoded_log["data"] = Web3.to_hex(value)
        elif key == "topics":
            decoded_log[key] = [Web3.to_hex(t) for t in value]
        elif isinstance(value, bytes):
            decoded_log[key] = Web3.to_hex(value)
        else:
            decoded_log[key] = value
    return decoded_log


###########
# Account #
###########
# Need to think on how to integrate this account in the genlayer accounts manager
# Is it possible to create a new account (there are only 20 now in web3.eth.accounts)
print("Get account")
# print("________________________")
# account = web3.eth.accounts[0]  # Use the first account
# print("Account:", account)
# private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"  # Need to get it somehow from the account
account = Account.create()
private_key = account.key.hex()
account = account.address
print("Account:", account)
print("private_key:", private_key)
print("Account Balance:", web3.eth.get_balance(account))


##################
# Ghost contract #
##################
# Do this only when a genlayer contract is deployed. Add contract_address to Transaction model database
print("\nCreate ghost contract")
print("________________________")

# Read contract ABI and bytecode from compiled contract
with open("hardhat/artifacts/contracts/GhostContract.sol/GhostContract.json", "r") as f:
    contract_json = json.loads(f.read())
    abi = contract_json["abi"]
    bytecode = contract_json["bytecode"]

# Create the contract instance
contact = web3.eth.contract(abi=abi, bytecode=bytecode)

# Build the transaction
gas_estimate = web3.eth.estimate_gas(
    contact.constructor().build_transaction(
        {
            "from": account,
            "nonce": web3.eth.get_transaction_count(account),
            "gasPrice": 0,
        }
    )
)
transaction = contact.constructor().build_transaction(
    {
        "from": account,
        "nonce": web3.eth.get_transaction_count(account),
        "gas": gas_estimate,
        "gasPrice": 0,
    }
)

# Sign the transaction
signed_tx = web3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
print(f"Transaction sent! Hash: {tx_hash.hex()}")

# Wait for the transaction receipt
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"eth_getTransactionReceipt: {json.dumps(decode_eth_dict(receipt), indent=2)}")
print(f"Contract deployed at address: {receipt.contractAddress}")
contract_address = receipt.contractAddress


######################
# Rollup transaction #
######################
# Do this every time we do transactions_processor.create_rollup_transaction(transaction.hash)
print("\nCreate rollup transaction")
print("________________________")

gas_estimate = web3.eth.estimate_gas(
    {
        "from": account,
        "to": contract_address,
        "value": 0,
        "data": web3.to_hex(text="todo: This should be genlayer data.."),
    }
)

transaction = {
    "from": account,
    "to": contract_address,
    "value": 0,
    "data": web3.to_hex(text="todo: This should be genlayer data.."),
    "nonce": web3.eth.get_transaction_count(account),
    "gas": gas_estimate,
    "gasPrice": 0,
}

# Sign and send the transaction
signed_tx = web3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

# Wait for transaction to be actually mined and get the receipt
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# View the Receipt
print("eth_getTransactionReceipt:", json.dumps(decode_eth_dict(receipt), indent=2))

# Get full transaction details including input data
transaction = web3.eth.get_transaction(tx_hash)
print("\neth_getTransactionByHash:", json.dumps(decode_eth_dict(transaction), indent=2))
print("\nDecoded input data:", web3.to_text(transaction["input"]))


print("Account Balance:", web3.eth.get_balance(account))
