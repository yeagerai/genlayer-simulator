from unittest.mock import patch, MagicMock


@patch('rpc.server.MessageHandler')
@patch('rpc.server.create_tables_if_they_dont_already_exist')
def test_create_tables_success(mock_create_tables, mock_message_handler):
    return_value = 'Dave'
    returned_data = {'status': 'success', 'data': return_value}

    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.success_response.return_value = returned_data

    mock_create_tables.return_value = return_value

    from rpc.server import create_tables

    response = create_tables()

    mock_create_tables.assert_called_once()
    mock_message_instance.success_response.assert_called_once_with(return_value)
    assert response == returned_data


@patch('rpc.server.MessageHandler')
@patch('rpc.server.create_tables_if_they_dont_already_exist')
def test_create_table_error(mock_create_tables, mock_message_handler):
    error_string = 'There was an error'
    exception_instance = Exception(error_string)
    returned_data = {'status': 'error', 'data': error_string}

    mock_create_tables.side_effect = exception_instance

    mock_message_instance = MagicMock()
    mock_message_handler.return_value = mock_message_instance
    mock_message_instance.error_response.return_value = returned_data

    from rpc.server import create_tables

    response = create_tables()

    mock_create_tables.assert_called_once()
    mock_message_instance.error_response.assert_called_once_with(exception=exception_instance)
    assert response == {'status': 'error', 'data': error_string}
