import json
from unittest.mock import patch, MagicMock

from common.urls import genvm_url
from common.testing.response.function import (
    has_success_status,
    has_data
)
from common.testing.db.base import setup_db_and_tables
from database.functions import DatabaseFunctions
from rpc.server import deploy_intelligent_contract

from_address = "0x1f9090aaE28b8a3dCeaDf281B0F12828e676c326"
contract_address = "0xc4440Bc34e9Af9cfEA4931614E8b56899fF286e4"
class_name = "WizardOfCoin"
contract_code = open("examples/contracts/wizard_of_coin.py").read()
genvm_response = open("rpc/tests/responses/genvm/deploy_contract.json").read()
contract_args = '{"have_coin": "True"}'
all_validators = open("rpc/tests/responses/db/all_validators.json").read()


def test_deploy_intelligent_contract():
    setup_db_and_tables()
    with patch("requests.post") as mock_post:
        with patch.dict('os.environ', {'NUMVALIDATORS': '2'}):
            with patch("consensus.utils.vrf") as mock_vrf:
                with patch("common.address.create_new_address") as mock_create_new_address:
                    with patch("database.functions.DatabaseFunctions") as MockDatabaseFunctions:

                        mock_dbf_instance = MagicMock()
                        MockDatabaseFunctions.__enter__.return_value = mock_dbf_instance
                        MockDatabaseFunctions.__exit__.return_value = False

                        mock_dbf_instance.all_validators.return_value = json.loads(all_validators)
                
                        mock_response = MagicMock()
                        mock_response.json.return_value = json.loads(genvm_response)
                        mock_post.return_value = mock_response

                        mock_vrf.return_value = json.loads(all_validators)[:2]

                        mock_create_new_address.return_value = contract_address

                        result = deploy_intelligent_contract(from_address, class_name, contract_code, contract_args)

                        assert has_success_status(result)
                        assert has_data(result)

                        mock_post.assert_called_once_with(
                            genvm_url() + "/api",
                            json={
                                "jsonrpc": "2.0",
                                "method": "deploy_contract",
                                "params": [from_address, contract_code, contract_args, class_name, all_validators[0]],
                                "id": 3,
                            }
                        )
