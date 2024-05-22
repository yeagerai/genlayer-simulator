import unittest
from unittest.mock import patch, MagicMock
from rpc.server import send_transaction

from_account = "0x5c9B872cFc6de9c33B777D43C6A5377C618115Ce"
to_account   = "0xc197fD93A12D7012241AC727756dAb0F76B39EC9"
amount       = 12.0


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
def test_send_transaction_error_from_account_in_wrong_format(
    mock_address_format,
    mock_message_handler
):
    # Data
    bad_account = "This is not an ethereum address"
    returned_data = {
        "status": "error",
        "message": "from_account not in ethereum address format",
        "data": {}
    }
    
    # Mocks
    mock_msg_instance = MagicMock()
    mock_message_handler.return_value = mock_msg_instance
    mock_msg_instance.error_response.return_value = returned_data

    mock_address_format.side_effect = [False, True]

    # Call the function
    result = send_transaction(bad_account, to_account, amount)

    # Assert
    mock_msg_instance.error_response.assert_called_once_with(message=returned_data["message"])
    assert result == returned_data


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
def test_send_transaction_error_to_account_in_wrong_format(
    mock_address_format,
    mock_message_handler
):
    # Data
    bad_account = "This is not an ethereum address"
    returned_data = {
        "status": "error",
        "message": "to_account not in ethereum address format",
        "data": {}
    }
    
    # Mocks
    mock_msg_instance = MagicMock()
    mock_message_handler.return_value = mock_msg_instance
    mock_msg_instance.error_response.return_value = returned_data

    mock_address_format.side_effect = [True, False]

    # Call the function
    result = send_transaction(from_account, bad_account, amount)

    # Assert
    mock_msg_instance.error_response.assert_called_once_with(message=returned_data["message"])
    assert result == returned_data


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
def test_send_transaction_error_from_account_does_not_exist(
    mock_database_functions,
    mock_address_format,
    mock_message_handler
):
    # Data
    returned_data = {
        "status": "error",
        "message": "from_account does not exist",
        "data": {}
    }

    # Mock
    mock_address_format.side_effect = [True, True]  # Both addresses are in correct format
    
    mock_dbf_instance = MagicMock()
    mock_database_functions.return_value.__enter__.return_value = mock_dbf_instance
    mock_dbf_instance.get_current_state.side_effect = [None, "<default>"]  # from_account does not exist, to_account exists
    
    mock_msg_instance = MagicMock()
    mock_message_handler.return_value = mock_msg_instance
    mock_msg_instance.error_response.return_value = returned_data

    # Call the function
    result = send_transaction(from_account, to_account, amount)

    # Assert the expected result
    mock_msg_instance.error_response.assert_called_once_with(message=returned_data["message"])
    assert result == returned_data


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
def test_send_transaction_error_to_account_does_not_exist(
    mock_database_functions,
    mock_address_format,
    mock_message_handler
):
    # Data
    returned_data = {
        "status": "error",
        "message": "to_account does not exist",
        "data": {}
    }

    # Mock
    mock_address_format.side_effect = [True, True]  # Both addresses are in correct format
    
    mock_dbf_instance = MagicMock()
    mock_database_functions.return_value.__enter__.return_value = mock_dbf_instance
    mock_dbf_instance.get_current_state.side_effect = ["<default>", None]  # to_account does not exist, to_account exists
    
    mock_msg_instance = MagicMock()
    mock_message_handler.return_value = mock_msg_instance
    mock_msg_instance.error_response.return_value = returned_data

    # Call the function
    result = send_transaction(from_account, to_account, amount)

    # Assert the expected result
    mock_msg_instance.error_response.assert_called_once_with(message=returned_data["message"])
    assert result == returned_data


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
def test_send_transaction_error_insufficient_funds(
    mock_database_functions,
    mock_address_format,
    mock_message_handler
):
    # Data
    returned_data = {
        "status": "error",
        "message": "insufficient funds",
        "data": {}
    }

    # Mock
    mock_address_format.side_effect = [True, True]  # Both addresses are in correct format
    
    mock_dbf_instance = MagicMock()
    mock_database_functions.return_value.__enter__.return_value = mock_dbf_instance
    mock_dbf_instance.get_current_state.side_effect = [
            {"data": '{"balance": 5.0}'},  # from_account
            "<default>"  # to_account
        ]
    
    mock_msg_instance = MagicMock()
    mock_message_handler.return_value = mock_msg_instance
    mock_msg_instance.error_response.return_value = returned_data

    # Call the function
    result = send_transaction(from_account, to_account, amount)

    # Assert the expected result
    mock_msg_instance.error_response.assert_called_once_with(message=returned_data["message"])
    assert result == returned_data


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
@patch('rpc.server.get_genlayer_db_connection')
def test_send_transaction_error_db_connection_failed(
    mock_db_connection,
    mock_database_functions,
    mock_address_format,
    mock_message_handler
):
    # Data
    exception_string = "Database connection failed"
    exception_instance = Exception(exception_string)
    returned_data = {
        "status": "error",
        "message": exception_string,
        "data": {}
    }

    # Mock
    mock_address_format.side_effect = [True, True]  # Both addresses are in correct format
    
    mock_dbf_instance = MagicMock()
    mock_database_functions.return_value.__enter__.return_value = mock_dbf_instance
    mock_dbf_instance.get_current_state.side_effect = [
            {"data": '{"balance": 25.0}'},  # from_account
            {"data": '{"balance": 20.0}'},  # to_account
        ]
    
    mock_msg_instance = MagicMock()
    mock_message_handler.return_value = mock_msg_instance
    mock_msg_instance.error_response.return_value = returned_data

    mock_db_connection.side_effect = exception_instance

    # Call the function
    result = send_transaction(from_account, to_account, amount)

    # Assert the expected result
    mock_msg_instance.error_response.assert_called_once_with(exception=exception_instance)
    assert result == returned_data


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
@patch('rpc.server.get_genlayer_db_connection')
def test_send_transaction_error_db_execute_exception(
    mock_db_connection,
    mock_database_functions,
    mock_address_format,
    mock_message_handler
):
    # Data
    exception_instance = Exception("<default>")
    error_string = "create the tables in the database first"
    returned_data = {
        "status": "error",
        "message": error_string,
        "data": {}
    }

    # Mock
    mock_address_format.side_effect = [True, True]  # Both addresses are in correct format
    
    mock_dbf_instance = MagicMock()
    mock_database_functions.return_value.__enter__.return_value = mock_dbf_instance
    mock_dbf_instance.get_current_state.side_effect = [
            {"data": '{"balance": 25.0}'},  # from_account
            {"data": '{"balance": 20.0}'},  # to_account
        ]

    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = [exception_instance, True, True]
    mock_db_connection.return_value = mock_connection

    mock_msg_instance = MagicMock()
    mock_message_handler.return_value = mock_msg_instance
    mock_msg_instance.error_response.return_value = returned_data

    # Call the function
    result = send_transaction(from_account, to_account, amount)

    # Assert the expected result
    mock_msg_instance.error_response.assert_called_once_with(exception=exception_instance)
    assert result == returned_data


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
@patch('rpc.server.get_genlayer_db_connection')
def test_send_transaction_success(
    mock_db_connection,
    mock_database_functions,
    mock_address_format,
    mock_message_handler
):
    # Data
    data = {
        'from_account': from_account,
        'to_account': to_account,
        'amount': amount
    }
    returned_data = {
        "status": "success",
        "message": "",
        "data": data
    }

    # Mock
    mock_address_format.side_effect = [True, True]  # Both addresses are in correct format
    
    mock_dbf_instance = MagicMock()
    mock_database_functions.return_value.__enter__.return_value = mock_dbf_instance
    mock_dbf_instance.get_current_state.side_effect = [
            {"data": '{"balance": 25.0}'},  # from_account
            {"data": '{"balance": 20.0}'},  # to_account
        ]

    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = [True, True, True]
    mock_db_connection.return_value = mock_connection

    mock_msg_instance = MagicMock()
    mock_message_handler.return_value = mock_msg_instance
    mock_msg_instance.success_response.return_value = returned_data

    # Call the function
    result = send_transaction(from_account, to_account, amount)

    # Assert the expected result
    mock_msg_instance.success_response.assert_called_once_with(data)
    assert result == returned_data
