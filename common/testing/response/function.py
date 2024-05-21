
def has_error_status(result: dict) -> bool:
    return result['status'] == 'error'

def has_success_status(result: dict) -> bool:
    return result['status'] == 'success'

def has_message(result:dict) -> bool:
    return 'message' in result

def has_data(result:dict) -> bool:
    return 'data' in result

def message_is(result:dict, message:dict) -> bool:
    return result['message'] == message

def data_is(result:dict, data:dict) -> bool:
    return result['data'] == data

def message_contains(result:dict, message:dict) -> bool:
    return message in result['message']

def data_contains(result:dict, data:dict) -> bool:
    return data in result['data']