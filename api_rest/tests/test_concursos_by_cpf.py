from app import app

def test_busca_concursos_cpf():
    client = app.test_client()

    response = client.get("/concursos/by_cpf/182.845.084-34")
    assert response.status_code in [200, 404]

    response = client.get("/concursos/by_cpf/311.667.973-47")
    assert response.status_code in [200, 404]

    response = client.get("/concursos/by_cpf/565.512.353-92")
    assert response.status_code in [200, 404]