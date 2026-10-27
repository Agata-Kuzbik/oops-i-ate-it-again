from database import get_all_products

def test_get_all_products():
    all_products = get_all_products()
    expected_keys = {"id", "name", "quantity", "unit", "expiry_date"}

    assert isinstance(all_products, list)
    assert all_products != []

    for product in all_products:
        assert isinstance(product, dict)
        assert expected_keys.issubset(product.keys())
        assert isinstance(product["name"], str)
        assert isinstance(product["quantity"], int)
        assert product["name"].strip() != ""
        assert isinstance(product["unit"], str)
        assert product["unit"].strip() != ""
     

    

    
    
    