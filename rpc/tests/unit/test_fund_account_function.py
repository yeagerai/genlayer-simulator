from unittest.mock import patch, MagicMock

account = "0x5c9B872cFc6de9c33B777D43C6A5377C618115Ce"
balance = 12.0


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
def test_fund_account_with_invalid_ethereum_address(mock_address_format, mock_message_handler):
    error_message = "account not in ethereum address format"
    returned_data = {
        "status": "error",
        "message": error_message,
        "data": {}
    }

    # Data
    test_account = "invalid_eth_address"
    test_balance = 100.0

    # Mock
    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.error_response.return_value = returned_data

    mock_address_format.return_value = False

    # Call the function
    from rpc.server import fund_account
    result = fund_account(test_account, test_balance)

    # Assert
    mock_address_format.assert_called_once_with(test_account)
    mock_message_instance.error_response.assert_called_once_with(message=error_message)
    assert result == returned_data


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
def test_fund_account_account_does_not_exist(mock_db_functions, mock_address_format, mock_message_handler):
    error_message = "account does not exist"
    returned_data = {
        "status": "error",
        "message": error_message,
        "data": {}
    }

    # Mocks
    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.error_response.return_value = returned_data

    mock_address_format.return_value = True

    mock_dbf_instance = MagicMock()
    mock_dbf_instance.__enter__.return_value = mock_dbf_instance
    mock_dbf_instance.get_current_state.return_value = None
    mock_db_functions.return_value = mock_dbf_instance

    # Call the function
    from rpc.server import fund_account
    result = fund_account(account, balance)

    # Assert
    mock_address_format.assert_called_once_with(account)
    mock_dbf_instance.get_current_state.assert_called_once()
    mock_message_instance.error_response.assert_called_once_with(message=error_message)
    assert result == returned_data


@patch('rpc.server.DatabaseFunctions')
@patch('rpc.server.get_genlayer_db_connection')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.MessageHandler')
def test_fund_account_failure(
    mock_message_handler,
    mock_address_format,
    mock_db_connection,
    mock_db_functions
):
    error_string = 'There was an error'
    exception_instance = Exception(error_string)
    returned_data = {'status': 'error', 'message': '', 'data': error_string}

    # Mock
    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.error_response.return_value = returned_data

    mock_dbf_instance = MagicMock()
    mock_dbf_instance.__enter__.return_value = mock_dbf_instance
    mock_dbf_instance.get_current_state.return_value = "something"
    mock_db_functions.return_value = mock_dbf_instance

    mock_connection = MagicMock()
    mock_db_connection.return_value = mock_connection
    mock_cursor = mock_connection.cursor.return_value

    mock_address_format.return_value = True

    mock_cursor.execute.side_effect = exception_instance

    # Call the function
    from rpc.server import fund_account
    result = fund_account(account, balance)

    # Assert
    mock_address_format.assert_called_once_with(account)
    mock_message_instance.error_response.assert_called_once_with(exception=exception_instance)

    assert result == returned_data


@patch('rpc.server.get_genlayer_db_connection')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
@patch('rpc.server.MessageHandler')
def test_fund_account_success(
    mock_message_handler,
    mock_db_functions,
    mock_address_format,
    mock_db_connection
):

    # Data
    returned_data = {
        'status': 'success',
        'message': '',
        'data': {
            'address': account,
            'balance': balance
        }
    }

    # Mock
    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.success_response.return_value = returned_data

    # (so it knows the address has funds)
    mock_dbf_instance = MagicMock()
    mock_dbf_instance.__enter__.return_value = mock_dbf_instance
    mock_dbf_instance.get_current_state.return_value = "something"
    mock_db_functions.return_value = mock_dbf_instance

    mock_connection = MagicMock()
    mock_db_connection.return_value = mock_connection
    mock_cursor = mock_connection.cursor.return_value

    mock_cursor.execute.return_value = None

    # Call the function
    from rpc.server import fund_account
    result = fund_account(account, balance)

    # Assert
    mock_address_format.assert_called_once_with(account)
    mock_dbf_instance.get_current_state.assert_called_once()
    mock_message_instance.success_response.assert_called_once_with(returned_data['data'])

    assert result == returned_data


@patch('rpc.server.get_genlayer_db_connection')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.create_account')
@patch('rpc.server.DatabaseFunctions')
@patch('rpc.server.MessageHandler')
def test_fund_account_success_new_address(
    mock_message_handler,
    mock_db_functions,
    mock_create_account,
    mock_address_format,
    mock_db_connection
):

    # Data
    create_account = "create_account"
    account_string = "0x5c9B872cFc6de9c33B777D43C6A5377C618115Ce"
    returned_data = {
        'status': 'success',
        'message': '',
        'data': {
            'address': account_string,
            'balance': balance
        }
    }
    create_account_returned_data = {
        'status': 'success',
        'message': '',
        'data': {
            'address': account_string,
            'balance': balance
        }
    }

    # Mock
    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.success_response.return_value = returned_data

    mock_dbf_instance = MagicMock()
    mock_dbf_instance.__enter__.return_value = mock_dbf_instance
    mock_dbf_instance.get_current_state.return_value = "something"
    mock_db_functions.return_value = mock_dbf_instance

    mock_connection = MagicMock()
    mock_db_connection.return_value = mock_connection
    mock_cursor = mock_connection.cursor.return_value

    mock_create_account.return_value = create_account_returned_data

    mock_cursor.execute.return_value = None

    # Call the function
    from rpc.server import fund_account
    result = fund_account(create_account, balance)

    # Assert
    mock_address_format.assert_called_once_with(create_account)
    mock_dbf_instance.get_current_state.assert_not_called()
    mock_message_instance.success_response.assert_called_once_with(returned_data['data'])

    assert result == returned_data


