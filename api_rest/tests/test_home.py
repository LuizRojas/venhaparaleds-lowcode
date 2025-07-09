from app import app

def test_home_status_code():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code in (200, 404)  # api disponivel?