import os
import random
from database.credentials import get_genlayer_db_connection
import json


def vrf(items, weights, k):
    weighted_indices = random.choices(range(len(items)), weights=weights, k=k * 10)
    unique_indices = set()
    random.shuffle(weighted_indices)

    for idx in weighted_indices:
        unique_indices.add(idx)
        if len(unique_indices) == k:
            break

    return [items[i] for i in unique_indices]


def get_contract_state(contract_address: str) -> dict: # that should be on the rpc and cli maybe
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT data FROM current_state WHERE id = (%s);", (contract_address,)
        )
        contract_row = cursor.fetchone()
        if contract_row is not None:
            contract_state = contract_row[0]
            return json.loads(contract_state)
        else:
            return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def genvm_url():
    return os.environ['GENVMPROTOCOL']+'://'+os.environ['GENVMHOST']+':'+os.environ['GENVMPORT']