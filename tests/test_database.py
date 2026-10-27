from database import get_all_products
from datetime import datetime

def test_get_all_products():
    all_products = get_all_products()
    expected_keys = {"id", "name", "quantity", "unit", "expiry_date"}
    expected_types = {
        "id": int,
        "name": str,
        "quantity": int,
        "unit": str,
        "expiry_date": str,
    }


    assert isinstance(all_products, list)
    assert all_products != []

    for product in all_products:
        assert isinstance(product, dict)
        assert expected_keys.issubset(product.keys())
        assert product["name"].strip() != ""
        assert product["unit"].strip() != ""
        assert product["expiry_date"].strip() != ""
        assert datetime.strptime(product["expiry_date"], "%Y-%m-%d")
        

        for key, expected_type in expected_types.items():
            assert isinstance(product[key], expected_type)

       
        
        
        
        
       
        
     

    

    
    
    