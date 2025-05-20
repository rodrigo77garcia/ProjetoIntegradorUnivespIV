from flask.testing import FlaskClient


def test_clientes_listagem(client: FlaskClient):
    response = client.get("/clientes")
    assert response.status_code == 200
    assert isinstance(response.json, list) or "html" in response.data.decode().lower()


def test_add_cliente(client: FlaskClient):
    response = client.post("/add_cliente", data={
        "nome": "João",
        "email": "joao@email.com"
    }, follow_redirects=True)
    assert response.status_code in [200, 201, 302]

    if response.is_json:
        data = response.get_json()
        assert data["message"] == "Cliente adicionado com sucesso"
    else:
        assert b"Cliente adicionado com sucesso!" in response.data