from app import app

def test_get_products():
    client = app.test_client()
    response = client.get("/api/products")
    data = response.get_json()

    expected_keys = {"id", "name", "quantity", "unit", "expiry_date"}


    assert response.status_code == 200
    assert isinstance(data, list)
    assert data != []

    for product in data:

        assert isinstance(product, dict)
        assert expected_keys.issubset(product.keys())
        assert isinstance(product["id"], int)
        assert isinstance(product["name"], str)
        assert isinstance(product["quantity"], int)
        assert isinstance(product["unit"], str)
        assert isinstance(product["expiry_date"], str)



def test_get_home():
    client = app.test_client()
    response = client.get("/")
    
    
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Oops! I Ate It Again!"
    


