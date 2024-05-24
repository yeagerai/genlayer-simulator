from unittest.mock import patch

from rpc.server import get_all_validators


@patch('rpc.server.MessageHandler')
@patch('rpc.server.DatabaseFunctions')
def test_get_all_validators_error_exception(mock_dbf, mock_msg_handler):
    # Data
    exception_string = "Database error"
    exception_instance = Exception(exception_string)
    return_data = {"status": "error", "message": exception_string}

    # Mock
    mock_dbf.return_value.__enter__.side_effect = exception_instance
    
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.error_response.return_value = return_data
    
    # Call the function
    response = get_all_validators()
    
    # Assertions
    assert response == return_data
    mock_msg_instance.error_response.assert_called_once_with(exception=exception_instance)


@patch('rpc.server.MessageHandler')
@patch('rpc.server.DatabaseFunctions')
def test_get_all_validators_success(mock_dbf, mock_msg_handler):
    # Data
    get_all_validators_response = "<default>"
    return_data = {"status": "success", "data": get_all_validators_response}

    # Mock
    mock_dbf_instance = mock_dbf.return_value.__enter__.return_value
    mock_dbf_instance.all_validators.return_value = get_all_validators_response
    
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.success_response.return_value = return_data
    
    # Call the function
    response = get_all_validators()
    
    # Assert
    assert response == return_data
    mock_dbf_instance.all_validators.assert_called_once()
    mock_msg_instance.success_response.assert_called_once_with(return_data['data'])

