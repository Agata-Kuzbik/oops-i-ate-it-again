from database import get_all_products, init_db, add_product, reset_database
from datetime import datetime
import pytest


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

       
def test_add_product():
    database = "test_inventory.db"
    init_db(database)
    reset_database(database)

    product = {
        "name": "Sok jabłkowy",
        "quantity": 1,
        "unit": "l",
        "expiry_date": "2027-04-13"
        }

    add_product(product, database)

    all_products = get_all_products(database)

    assert len(all_products) == 1
    assert all_products[0]["name"] == "Sok jabłkowy"
    assert all_products[0]["quantity"] == 1
    assert all_products[0]["unit"] == "l"
    assert all_products[0]["expiry_date"] == "2027-04-13"


def test_add_product_without_name():

    product = {
        "quantity": 1,
        "unit": "l",
        "expiry_date": "2027-04-13"
        }

    with pytest.raises(KeyError):
        add_product(product, "test_inventory.db")

def test_add_product_with_invalid_name_type():

    product = {
            "name": 123,
            "quantity": 1,
            "unit": "l",
            "expiry_date": "2027-04-13"
            }
    
    with pytest.raises(TypeError):
        add_product(product, "test_inventory.db")

def test_add_product_with_empty_name():

    product = {
            "name": "",
            "quantity": 1,
            "unit": "l",
            "expiry_date": "2027-04-13"
            }
        
    with pytest.raises(ValueError):
        add_product(product, "test_inventory.db")

def test_add_product_with_whitespace_name():

    product = {
            "name": "  ",
            "quantity": 1,
            "unit": "l",
            "expiry_date": "2027-04-13"
            }
     
    with pytest.raises(ValueError):
        add_product(product, "test_inventory.db")
      

        
       
        
     

    

    
    
    