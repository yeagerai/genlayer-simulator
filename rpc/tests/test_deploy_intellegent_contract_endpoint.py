from unittest.mock import patch, MagicMock

from common.address import create_new_address

class_name = "WizardOfCoin"
contract_code


def test_deploy_intelligent_contract():
    with patch("requests.post") as mock_post:
        # Mocking the response object
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": {
                "status": "success",
                "data": {
                    "contract_state": "some_state"
                }
            }
        }
        mock_post.return_value = mock_response

        # Call the function with sample arguments
        result = deploy_intelligent_contract(create_new_address(), class_name, "contract_code", "constructor_args")

        # Assert the function's behavior based on the mocked response
        assert result == {'contract_id': mock_contract_id}

        # Assert that requests.post was called with the correct arguments
        mock_post.assert_called_once_with(
            "mocked_genvm_url/api",
            json={
                "jsonrpc": "2.0",
                "method": "deploy_contract",
                "params": ["from_account", "contract_code", "constructor_args", "class_name", "leader_config"],
                "id": 3,
            }
        )
