from unittest.mock import patch, MagicMock


@patch('rpc.server.create_new_address')
@patch('rpc.server.get_genlayer_db_connection')
@patch('rpc.server.MessageHandler')
def test_create_account_success(mock_message_handler, mock_db_connection, mock_create_new_address):
    # Setup
    test_address = "1234567890abcdef"
    mock_create_new_address.return_value = test_address

    returned_data = {
        "status": "success",
        "message": "",
        "data": {
            "address": test_address,
            "balance": 0
        }
    }
    
    # Mock database connection and cursor
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_db_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    # Mock MessageHandler
    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.success_response.return_value = returned_data
    
    # Execution
    from rpc.server import create_account
    result = create_account()

    # Assert
    mock_create_new_address.assert_called_once()
    mock_db_connection.assert_called_once()
    mock_cursor.execute.assert_called_once()
    mock_connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()
    assert result == returned_data


@patch('rpc.server.create_new_address')
@patch('rpc.server.get_genlayer_db_connection')
@patch('rpc.server.MessageHandler')
def test_create_account_failure(mock_message_handler, mock_db_connection, mock_create_new_address):
    # Setup
    mock_create_new_address.return_value = "1234567890abcdef"
    exception_message = "Database error"
    exception_instance = Exception(exception_message)

    returned_data = {
        "status": "error",
        "message": exception_message,
        "data": {}
    }
    
    # Mock database connection and cursor
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_db_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = exception_instance

    # Mock MessageHandler
    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.error_response.return_value = returned_data

    # Execution
    from rpc.server import create_account
    result = create_account()

    # Assert
    mock_create_new_address.assert_called_once()
    mock_db_connection.assert_called_once()
    mock_cursor.execute.assert_called_once()
    mock_connection.commit.assert_not_called()
    mock_cursor.close.assert_not_called()
    mock_connection.close.assert_not_called()
    assert result == returned_data