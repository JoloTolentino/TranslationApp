from server import create_app
import pytest


def test_signup_valid_user(client):
    user_data = {
        "username": "testuser",
        "firstname": "test",
        "lastname": "Tester",
        "email": "test@example.com",
        "password": "SuperSecret123",
        "subscription": "basic"
    }
    response = client.post('/signup', json=user_data)
    assert response.status_code == 200



def test_signup_missing_keys(client):
    user_data = {
        "username": "jarytolentino",
        "email": "jary@example.com"
    }

    response = client.post('/signup', json=user_data)
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'missing_keys' in json_data


