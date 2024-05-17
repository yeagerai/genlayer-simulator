import json

from database.credentials import get_genlayer_db_connection


class DatabaseFunctions:

    def __init__(self):
        self.connection = get_genlayer_db_connection()
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()
    
    def validator_details(self, validator) -> dict:
        return {
            'id': validator[0],
            'address': validator[1],
            'stake': float(validator[2]),
            'provider': validator[3],
            'model': validator[4],
            'config': validator[5],
            'updated_at': validator[6].strftime("%m/%d/%Y %H:%M:%S")
        }

    def transaction_details(self, transaction) -> dict:
        return {
            'id': transaction[0],
            'from_address': transaction[1],
            'to_address': transaction[2],
            'input_data': json.dumps(transaction[3]),
            'data': json.dumps(transaction[4]),
            'consensus_data': json.dumps(transaction[5]),
            'nonce': transaction[6],
            'value': transaction[7],
            'type': transaction[8],
            'gaslimit': transaction[9],
            'created_at': transaction[10].strftime("%m/%d/%Y %H:%M:%S"),
            'r': transaction[11],
            's': transaction[12],
            'v': transaction[13]
        }
    
    def current_state_details(self, current_state) -> dict:
        return {
            'id': current_state[0],
            'data': json.dumps(current_state[1]),
            'updated_at': current_state[2].strftime("%m/%d/%Y %H:%M:%S")
        }
    
    def transaction_audit_details(self, transaction_audit) -> dict:
        return {
            'id': transaction_audit[0],
            'transaction_id': transaction_audit[1],
            'status': transaction_audit[2],
            'transaction_data': transaction_audit[3],
            'created_at': transaction_audit[4].strftime("%m/%d/%Y %H:%M:%S")
        }


    ### VALIDATORS ###

    def create_validator(self, address:str, stake:int, provider:str, model:str, config:json):
        self.cursor.execute(
            "INSERT INTO current_state (id, data) VALUES (%s, %s);", (address, json.dumps({'stake':stake}))
        )
        self.cursor.execute(
            "INSERT INTO validators (address, stake, provider, model, config, created_at) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP);",
            (address, stake, provider, model, config),
        )
        self.connection.commit()
        return self.get_validator(address)

    def delete_validator(self, address:str):
        self.cursor.execute(
            "DELETE FROM validators WHERE address = %s;",
            (address,),
        )
        self.connection.commit()
        return {}

    def update_validator(self, validator_address:str, stake:float, provider:str, model:str, config:json):
        self.cursor.execute(
            "UPDATE validators SET stake = %s, provider = %s, model = %s, config = %s, created_at = CURRENT_TIMESTAMP WHERE address = %s;",
            (stake, provider, model, config, validator_address),
        )
        self.connection.commit()
        return self.get_validator(validator_address)

    def get_validator(self, address:str):
        self.cursor.execute("SELECT * FROM validators WHERE address = %s", (address,))
        self.connection.commit()
        validator = self.cursor.fetchone()
        if validator:
            return self.validator_details(validator)
        else:
            return {}

    def all_validators(self):
        self.cursor.execute("SELECT * FROM validators")
        self.connection.commit()
        validators = []
        for validator in self.cursor.fetchall():
            validators.append(self.validator_details(validator))
        return validators


    ### TRANSACTIONS ###

    def insert_transaction(
            self,
            from_address:str,
            to_address:str,
            data:json,
            type:int,
            value:int,
            input_data:json=None,
            consensus_data:json=None,
            nonce:int=None,
            gaslimit:int=None,
            r:int=None,
            s:int=None,
            v:int=None):
        self.cursor.execute(
            "INSERT INTO transactions (from_address, to_address, data, type, value, input_data, consensus_data, nonce, gaslimit, r, s, v) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;",
            (from_address, to_address, data, type, value, input_data, consensus_data, nonce, gaslimit, r, s, v),
        )
        self.connection.commit()
        new_row_id = self.cursor.fetchone()[0]
        return self.get_transaction(new_row_id)


    def get_transaction(self, transaction_id:int):
        self.cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
        self.connection.commit()
        transaction = self.cursor.fetchone()
        if transaction:
            return self.transaction_details(transaction)
        else:
            return None


    ### CURRENT STATE ###

    def insert_current_state(self, id:str, data:json):
        self.cursor.execute(
            "INSERT INTO current_state (id, data) VALUES (%s, %s) RETURNING id;",
            (id, data),
        )
        self.connection.commit()
        current_state_id = self.cursor.fetchone()[0]
        return self.get_current_state(current_state_id)


    def get_current_state(self, id:str):
        self.cursor.execute("SELECT * FROM current_state WHERE id = %s", (id,))
        self.connection.commit()
        current_state = self.cursor.fetchone()
        if current_state:
            return self.current_state_details(current_state)
        else:
            return None

    def update_current_state(self, id:str, data:json):
        self.cursor.execute(
            "UPDATE current_state SET data = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s;",
            (data, id),
        )
        self.connection.commit()
        return self.get_current_state(id)


    ### TRANSACTION AUDIT ###

    def insert_transaction_audit(self, transaction_id:int, status:str, transaction_data:str):
        self.cursor.execute(
            "INSERT INTO transactions_audit (transaction_id, status, transaction_data) VALUES (%s, %s, %s);",
            (transaction_id, status, transaction_data),
        )
        self.connection.commit()
        return self.get_transaction_audit(transaction_id)

    def get_transaction_audit(self, transaction_id:int):
        self.cursor.execute("SELECT * FROM transactions_audit WHERE transaction_id = %s", (transaction_id,))
        self.connection.commit()
        audit_entries = []
        for audit in self.cursor.fetchall():
            audit_entries.append(self.transaction_audit_details(audit))
        return audit_entries

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
