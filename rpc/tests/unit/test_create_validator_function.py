from unittest.mock import patch

from rpc.server import create_validator

input_data = {
    "stake": 12.5,
    "provider": "ollama",
    "model": "llama3",
    "config": {}
}


@patch('rpc.server.get_providers_and_models')
@patch('rpc.server.MessageHandler')
def test_create_validator_error_provider_not_avaliable(
    mock_msg_handler,
    mock_get_providers_and_models
):
    # Data
    return_data = {"status": "error", "data": "", "message": "Provider not available"}
    providers_and_models_data = {"data": {"<default>": []}}

    # Mock
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.error_response.return_value = return_data

    mock_get_providers_and_models.return_value = providers_and_models_data
    
    # Call the function
    response = create_validator(**input_data)
    
    # Assertions
    assert response == return_data
    mock_get_providers_and_models.assert_called_once()
    mock_msg_instance.error_response.assert_called_once_with(message=return_data['message'])


@patch('rpc.server.get_providers_and_models')
@patch('rpc.server.MessageHandler')
def test_create_validator_error_model_not_avaliable(
    mock_msg_handler,
    mock_get_providers_and_models
):
    # Data
    return_data = {"status": "error", "data": "", "message": "Model not available"}
    providers_and_models_data = {"data": {"ollama": ["<default>"]}}

    # Mock
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.error_response.return_value = return_data

    mock_get_providers_and_models.return_value = providers_and_models_data
    
    # Call the function
    response = create_validator(**input_data)
    
    # Assertions
    assert response == return_data
    mock_get_providers_and_models.assert_called_once()
    mock_msg_instance.error_response.assert_called_once_with(message=return_data['message'])


@patch('rpc.server.get_providers_and_models')
@patch('rpc.server.MessageHandler')
@patch('rpc.server.DatabaseFunctions')
def test_create_validator_error_database_exception(
    mock_dbf,
    mock_msg_handler,
    mock_get_providers_and_models
):
    # Data
    exception_string = "Database error"
    exception_instance = Exception(exception_string)
    return_data = {"status": "error", "data": "", "message": exception_string}

    # Mock
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.error_response.return_value = return_data

    mock_get_providers_and_models.return_value = {"data": {"ollama": ["llama3"]}}

    mock_dbf.return_value.__enter__.side_effect = exception_instance
    
    # Call the function
    response = create_validator(**input_data)
    
    # Assertions
    assert response == return_data
    mock_get_providers_and_models.assert_called_once()
    mock_msg_instance.error_response.assert_called_once_with(exception=exception_instance)


@patch('rpc.server.get_providers_and_models')
@patch('rpc.server.MessageHandler')
@patch('rpc.server.DatabaseFunctions')
@patch('rpc.server.get_validator')
def test_create_validator_success(
    mock_get_validator,
    mock_dbf,
    mock_msg_handler,
    mock_get_providers_and_models
):
    # Data
    return_data = {"status": "error", "data": "", "message": "Model not available"}
    providers_and_models_data = {"data": {"ollama": ["<default>"]}}

    # Mock
    mock_msg_instance = mock_msg_handler.return_value
    mock_msg_instance.error_response.return_value = return_data

    mock_get_providers_and_models.return_value = providers_and_models_data

    mock_dbf_instance = mock_dbf.return_value.__enter__.return_value
    mock_dbf_instance.create_validator.return_value = True
    
    # Call the function
    response = create_validator(**input_data)
    
    # Assertions
    assert response == return_data
    mock_get_providers_and_models.assert_called_once()
    mock_msg_instance.error_response.assert_called_once_with(message=return_data['message'])
