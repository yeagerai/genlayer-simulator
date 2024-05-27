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
            "id": validator[0],
            "address": validator[1],
            "stake": float(validator[2]),
            "provider": validator[3],
            "model": validator[4],
            "config": validator[5],
            "updated_at": validator[6].strftime("%m/%d/%Y, %H:%M:%S"),
        }

    def all_validators(self):
        self.cursor.execute("SELECT * FROM validators")
        self.connection.commit()
        validators = []
        for validator in self.cursor.fetchall():
            validators.append(self.validator_details(validator))
        return validators

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
