from app import app

def test_get_products():
    client = app.test_client()
    response =client.get("/api/products")
    data = response.get_json()

    expected_keys = {"id", "name", "quantity", "unit", "expiry_date"}


    assert response.status_code == 200
    assert isinstance(data, list)
    assert data != []

    product = data[0]

    assert isinstance(data[0], dict)
    assert expected_keys.issubset(product.keys())
    assert isinstance(product["name"], str)
    assert isinstance(product["quantity"], int)
    