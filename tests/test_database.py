from database import get_all_products

def test_get_all_products():
    all_products = get_all_products()
    print(all_products)

    expected_keys = {"id", "name", "quantity", "unit", "expiry_date"}

    assert isinstance(all_products, list)
    assert all_products != []
    assert isinstance(all_products[0], dict)
    assert expected_keys.issubset(all_products[0].keys())
    