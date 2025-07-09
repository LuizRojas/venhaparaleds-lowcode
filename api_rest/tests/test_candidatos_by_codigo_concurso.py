from app import app

def test_busca_candidatos_codigo():
    client = app.test_client()

    response = client.get("/candidatos/by_codigo_concurso/61828450843")
    assert response.status_code == 200

    response = client.get("/candidatos/by_codigo_concurso/61828450842")
    assert response.status_code == 200

    response = client.get("/candidatos/by_codigo_concurso/95655123539") # paulo pereira
    assert response.status_code == 200