import os

import pytest
from app import create_app


@pytest.fixture
def client():
    os.environ["{}_env"] = "testing"
    client = create_app().test_client()
    yield client

    # with client.app_context():
    #     flaskr.init_db()


def test_ping_api(client):
    rv = client.get('/ping/')
    assert b'message' in rv.data


def test_demo_get_api(client):
    rv = client.get('/api/v1/demo-api/')
    assert b'message' in rv.data


def test_demo_post_api(client):
    rv = client.post('/api/v1/demo-api/')
    assert b'message' in rv.data