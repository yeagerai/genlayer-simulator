from tests.common.requests import payload, post_request
from dotenv import load_dotenv

load_dotenv()


validator_keys = ['id', 'address', 'stake', 'provider','model', 'config', 'updated_at']


def test_create_db_and_tables():
    post_request(payload('create_db'))
    post_request(payload('create_tables'))
    assert True

def test_create_random_validator():
    stake = 10
    response = post_request(payload('create_random_validator', stake)).json()
    assert response['result']['status'] == 'success'
    assert response['result']['data']['stake'] == stake
    for key in validator_keys:
        assert key in response['result']['data']

def test_delete_validator_does_not_exist():
    validator_address = 'dave'
    response = post_request(payload('delete_validator', validator_address)).json()
    assert response['result']['status'] == 'error'
    assert response['result']['message'] == 'validator ' + validator_address + ' not found'

def test_delete_validator():
    new_validator = post_request(payload('create_random_validator', 10)).json()
    response = post_request(payload('delete_validator', new_validator['result']['data']['address'])).json()
    assert response['result']['status'] == 'success'
    assert response['result']['data'] == new_validator['result']['data']['address']

def test_get_validator_does_not_exist():
    validator_address = 'dave'
    response = post_request(payload('get_validator', validator_address)).json()
    assert response['result']['status'] == 'error'
    assert response['result']['message'] == 'validator ' + validator_address + ' not found'

def test_get_validator():
    new_validator = post_request(payload('create_random_validator', 10)).json()
    response = post_request(payload('get_validator', new_validator['result']['data']['address'])).json()
    assert response['result']['status'] == 'success'
    for key in new_validator['result']['data']:
        assert key in response['result']['data']
    post_request(payload('delete_validator', new_validator['result']['data']['address']))

def test_get_and_delete_all_validator():
    num_validators = 10
    # delete all validators first
    delete_reponse = post_request(payload('delete_all_validators')).json()
    assert delete_reponse['result']['status'] == 'success'
    new_validator_addresses = []
    # create new validators
    for validator in range(num_validators):
        response = post_request(payload('create_random_validator', 10)).json()
        new_validator_addresses.append(response['result']['data']['address'])
    response = post_request(payload('get_all_validators')).json()
    assert response['result']['status'] == 'success'
    # check that all validators exist
    for validator in response['result']['data']:
        assert validator['address'] in new_validator_addresses
    # delete all validators
    for validator in new_validator_addresses:
        post_request(payload('delete_validator', validator))
    # make sure all validators are deleted
    response = post_request(payload('get_all_validators')).json()
    assert len(response['result']['data']) == 0

def test_create_validator():
    data = {
        'stake': 8.0,
        'provider': 'openai',
        'model': 'gpt-3.5-turbo',
        'config': {'name': 'james'}
    }
    new_validator = post_request(
        payload(
            'create_validator',
            data['stake'],
            data['provider'],
            data['model'],
            data['config']
        )
    ).json()
    for key, value in data.items():
        assert key in new_validator['result']['data']
        assert value == new_validator['result']['data'][key]
    post_request(payload('delete_validator', new_validator['result']['data']['address']))

def test_update_validator_validator_does_not_exist():
    new_address = 'dave'
    data = {
        'stake': 12.0,
        'provider': 'test-1',
        'model': 'test-2',
        'config': {'test': 'test-3'}
    }
    updated_validator = post_request(
        payload(
            'update_validator',
            new_address,
            data['stake'],
            data['provider'],
            data['model'],
            data['config']
        )
    ).json()
    assert updated_validator['result']['status'] == 'error'
    assert updated_validator['result']['message'] == 'validator ' + new_address + ' not found'

def test_update_validator():
    new_validator = post_request(payload('create_random_validator', 10)).json()
    new_address = new_validator['result']['data']['address']
    data = {
        'stake': 12.0,
        'provider': 'test-1',
        'model': 'test-2',
        'config': {'test': 'test-3'}
    }
    updated_validator = post_request(
        payload(
            'update_validator',
            new_address,
            data['stake'],
            data['provider'],
            data['model'],
            data['config']
        )
    ).json()
    for key, value in data.items():
        assert key in updated_validator['result']['data']
        assert value == updated_validator['result']['data'][key]
    post_request(payload('delete_validator', new_address))