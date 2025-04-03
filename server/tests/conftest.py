

import pytest
from server import create_app  
from server.config import CONFIG
from server.extensions import db


@pytest.fixture(scope="session")
def base_url():
    return CONFIG.BASE_URL

@pytest.fixture
def client():
    app = create_app(testing=True)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client


