import pytest
import requests
from app import create_app
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch("requests.post")
def test_chat_success(mock_post, client):
    # Mock da resposta da API da Together
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "Isso é uma resposta de teste."
            }
        }]
    }
    mock_post.return_value = mock_response

    response = client.post("/chat", json={"message": "Olá"})
    assert response.status_code == 200
    assert response.is_json
    assert "response" in response.json
    assert response.json["response"] == "Isso é uma resposta de teste."

@patch("requests.post")
def test_chat_error(mock_post, client):
    # Simula uma exceção de rede (RequestException)
    mock_post.side_effect = requests.exceptions.RequestException("Erro simulado")

    response = client.post("/chat", json={"message": "Olá"})
    assert response.status_code == 500
    assert response.is_json
    assert "error" in response.json
    assert "Erro simulado" in response.json["error"]
