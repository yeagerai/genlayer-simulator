from unittest.mock import patch

from rpc.server import get_validator

validator_address = "0x9B9e5bADfbDca2B8B5DCCdFfEfa605Dc44B04f8F"


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
def test_get_validator_error_address_in_wrong_format(mock_dbf, mock_address_format, mock_msg_handler):
    # Data
    message = "validator address not in ethereum address format"
    return_data = {"status": "error", "message": message, "data": ""}

    # Mock
    mock_address_format.return_value = False
    
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.error_response.return_value = return_data
    
    # Call the function
    response = get_validator("this is not an eth address")
    
    # Assertions
    assert response == return_data
    mock_msg_instance.error_response.assert_called_once_with(message=message)


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
def test_get_validator_error_exception(mock_dbf, mock_address_format, mock_msg_handler):
    # Data
    exception_string = 'Database error'
    exception_instance = Exception(exception_string)
    return_data = {"status": "error", "message": exception_string, "data": ""}

    # Mock
    mock_dbf_instance = mock_dbf.return_value.__enter__.return_value
    mock_dbf_instance.get_validator.side_effect = exception_instance

    mock_address_format.return_value = True
    
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.error_response.return_value = return_data
    
    # Call the function
    response = get_validator(validator_address)
    
    # Assertions
    assert response == return_data
    mock_msg_instance.error_response.assert_called_once_with(exception=exception_instance)


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
def test_get_validator_error_no_validator_data(mock_dbf, mock_address_format, mock_msg_handler):
    # Data
    get_validator_response = {}
    function_response = f"validator {validator_address} not found"
    return_data = {"status": "success", "messages": "", "data": get_validator_response}

    # Mock
    mock_dbf_instance = mock_dbf.return_value.__enter__.return_value
    mock_dbf_instance.get_validator.return_value = get_validator_response

    mock_address_format.return_value = True
    
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.error_response.return_value = return_data
    
    # Call the function
    response = get_validator(validator_address)
    
    # Assert
    assert response == return_data
    mock_dbf_instance.get_validator.assert_called_once_with(validator_address)
    mock_msg_instance.error_response.assert_called_once_with(message=function_response)


@patch('rpc.server.MessageHandler')
@patch('rpc.server.address_is_in_correct_format')
@patch('rpc.server.DatabaseFunctions')
def test_get_validator_success(mock_dbf, mock_address_format, mock_msg_handler):
    # Data
    get_validator_response = "<default>"
    return_data = {"status": "success", "messages": "", "data": get_validator_response}

    # Mock
    mock_dbf_instance = mock_dbf.return_value.__enter__.return_value
    mock_dbf_instance.get_validator.return_value = get_validator_response

    mock_address_format.return_value = True
    
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.success_response.return_value = return_data
    
    # Call the function
    response = get_validator(validator_address)
    
    # Assert
    assert response == return_data
    mock_dbf_instance.get_validator.assert_called_once_with(validator_address)
    mock_msg_instance.success_response.assert_called_once_with(return_data['data'])

