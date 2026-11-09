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
        assert type(product["quantity"]) in (int, float)
        assert isinstance(product["unit"], str)
        assert isinstance(product["expiry_date"], str)



def test_get_home():
    client = app.test_client()
    response = client.get("/")

    html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Oops! I Ate It Again!" in html
    assert "Product name:" in html
    assert "Quantity:" in html
    assert "Unit:" in html
    assert "Expiry date:" in html
    assert "Add product" in html


