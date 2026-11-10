from app import app
from database import get_all_products, add_product

def test_get_products(database):
    client = app.test_client()
    original_database = app.config["DATABASE"]
    app.config["DATABASE"] = database

    try:
        product = {
            "name": "Milk",
            "quantity": 1,
            "unit": "l",
            "expiry_date": "2027-12-31"
            }
        add_product(product, database)
        response = client.get("/api/products")
        data = response.get_json()

        expected_keys = {"id", "name", "quantity", "unit", "expiry_date"}


        assert response.status_code == 200
        assert isinstance(data, list)
        assert data != []

        assert isinstance(data[0], dict)
        assert expected_keys.issubset(data[0].keys())
        assert isinstance(data[0]["id"], int)
        assert isinstance(data[0]["name"], str)
        assert data[0]["name"] == "Milk"
        assert type(data[0]["quantity"]) in (int, float)
        assert data[0]["quantity"] == 1
        assert isinstance(data[0]["unit"], str)
        assert data[0]["unit"] == "l"
        assert isinstance(data[0]["expiry_date"], str)
        assert data[0]["expiry_date"] == "2027-12-31"

    finally:
        app.config["DATABASE"] = original_database

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

def test_add_product(database):
    client = app.test_client()
    original_database = app.config["DATABASE"]
    app.config["DATABASE"] = database
    try:
        response = client.post("/products", data={
            "name": "Milk",
            "quantity": "1",
            "unit": "l",
            "expiry_date": "2027-12-31"
        })

        products = get_all_products(database)

        assert response.status_code == 302
        assert products[0]["name"] == "Milk"
        assert products[0]["quantity"] == 1.0
        assert products[0]["unit"] == "l"
        assert products[0]["expiry_date"] == "2027-12-31"

    finally:
        app.config["DATABASE"] = original_database


