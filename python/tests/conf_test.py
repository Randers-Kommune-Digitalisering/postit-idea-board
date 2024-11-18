import pytest
import tempfile
from main import create_app
from sqliteClient import init_db, SQLiteClient


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DATABASE": tempfile.NamedTemporaryFile(delete=False).name,  # Use temporary file for testing
    })

    with app.app_context():
        init_db(SQLiteClient(app.config["DATABASE"]))  # Initialize the database with temporary file

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_healthz(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'success'


def test_metrics(client):
    # POD_NAME env var set in pytest.ini (test-pod)
    response = client.get('/metrics')
    assert response.status_code == 200
    assert 'is_ready gauge\nis_ready{error_type="None",job_name="test-pod"} 1.0' in response.text
