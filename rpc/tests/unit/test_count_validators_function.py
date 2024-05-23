import unittest
from unittest.mock import patch, MagicMock

from rpc.server import count_validators


@patch('rpc.server.MessageHandler')
@patch('rpc.server.DatabaseFunctions')
def test_count_validators_exception(mock_dbf, mock_msg_handler):
    # Data
    exception_instance = Exception('Database error')
    return_data = {"status": "error", "message": "Database error"}

    # Mock
    mock_dbf.return_value.__enter__.side_effect = exception_instance
    
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.error_response.return_value = return_data
    
    # Call the function
    response = count_validators()
    
    # Assertions
    assert response == return_data
    mock_msg_instance.error_response.assert_called_once()


@patch('rpc.server.MessageHandler')
@patch('rpc.server.DatabaseFunctions')
def test_count_validators_success(mock_dbf, mock_msg_handler):
    # Data
    return_data = {"status": "success", "data": {"count": 3}}

    # Mock
    mock_dbf_instance = mock_dbf.return_value.__enter__.return_value
    mock_dbf_instance.all_validators.return_value = ['validator1', 'validator2', 'validator3']
    
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.success_response.return_value = return_data
    
    # Call the function
    response = count_validators()
    
    # Assert
    assert response == return_data
    mock_dbf_instance.all_validators.assert_called_once()
    mock_msg_instance.success_response.assert_called_once_with(return_data['data'])

