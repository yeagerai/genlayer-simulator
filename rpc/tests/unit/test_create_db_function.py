from unittest.mock import patch, MagicMock


@patch('rpc.server.MessageHandler')
@patch('rpc.server.create_db_if_it_doesnt_already_exists')
def test_create_db_success(mock_create_db, mock_message_handler):
    return_value = 'Dave'
    returned_data = {'status': 'success', 'data': return_value}

    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.success_response.return_value = returned_data

    mock_create_db.return_value = return_value

    from rpc.server import create_db

    response = create_db()

    mock_create_db.assert_called_once()
    mock_message_instance.success_response.assert_called_once_with(return_value)
    assert response == {'status': 'success', 'data': return_value}

@patch('rpc.server.MessageHandler')
@patch('rpc.server.create_db_if_it_doesnt_already_exists')
def test_create_db_error(mock_create_db, mock_message_handler):
    error_string = 'There was an error'
    exception_instance = Exception(error_string)
    returned_data = {'status': 'error', 'data': error_string}

    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.error_response.return_value = returned_data

    mock_create_db.side_effect = exception_instance

    from rpc.server import create_db

    response = create_db()
    print(response)

    mock_create_db.assert_called_once()
    mock_message_instance.error_response.assert_called_once()
    mock_message_instance.error_response.assert_called_with(exception=exception_instance)
    assert response == {'status': 'error', 'data': error_string}
