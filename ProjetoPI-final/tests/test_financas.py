import json

def test_listar_financas(client, mocker):
    # Mockando o cursor do banco
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchall.return_value = [
        {"id": 1, "descricao": "Receita A", "valor": 1000.0},
        {"id": 2, "descricao": "Despesa B", "valor": -500.0}
    ]

    mock_db = mocker.MagicMock()
    mock_db.cursor.return_value = mock_cursor
    mocker.patch("app.routes.get_db", return_value=mock_db)

    response = client.get("/listar_financas", headers={"Accept": "application/json"})

    assert response.status_code == 200
    data = response.get_json()

    assert response.status_code == 200, f"Status: {response.status_code}, Data: {response.get_data(as_text=True)}"
    assert isinstance(data, list)
    assert data[0]["descricao"] == "Receita A"
    assert data[1]["valor"] == -500.0
    assert len(data) == 2

