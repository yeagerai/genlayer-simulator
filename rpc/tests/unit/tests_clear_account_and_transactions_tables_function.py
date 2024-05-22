from unittest.mock import patch, MagicMock


@patch('rpc.server.app', new_callable=MagicMock)
@patch('rpc.server.socketio', new_callable=MagicMock)
@patch('rpc.server.MessageHandler')
@patch('rpc.server.clear_db_tables')
def test_create_tables_success(mock_clear_db_tables, mock_message_handler, mock_app, mock_socketio):
    return_value = 'cleared successfully'
    returned_data = {
        "status": "success",
        "message": '',
        "data": return_value
    }

    # Mocks
    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.success_response.return_value = returned_data

    mock_clear_db_tables.return_value = return_value

    # Call the functtion
    from rpc.server import clear_account_and_transactions_tables
    response = clear_account_and_transactions_tables()

    # Assert
    mock_clear_db_tables.assert_called_once()
    mock_message_instance.success_response.assert_called_once_with(return_value)
    assert response == returned_data
