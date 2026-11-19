from database import get_all_products, add_product
from datetime import datetime, date, timedelta
import pytest


def test_get_all_products(database):

    products_list = [
        {"name": "Milk", "quantity": 1, "unit": "l", "expiry_date": "2027-04-13"},
        {"name": "Flour", "quantity": 0.5, "unit": "kg", "expiry_date": "2028-06-16"},
        {"name": "Chips", "quantity": 5, "unit": "bags", "expiry_date": "2029-09-26"},
    ]
    expected_keys = {"id", "name", "quantity", "unit", "expiry_date"}
    expected_types = {
            "id": int,
            "name": str,
            "quantity": float,
            "unit": str,
            "expiry_date": str,
        }

    for product in products_list:
        add_product(product, database)
    all_products = get_all_products(database)

    assert isinstance(all_products, list)
    assert len(all_products) == len(products_list)
    assert len([product["id"] for product in all_products]) == len(set([product["id"] for product in all_products]))
    assert sorted(products_list, key= lambda product: product["name"]) == [{key: value for key, value in product.items() if key != "id"} for product in all_products]
    assert [product["name"] for product in sorted(products_list, key= lambda product: product["name"])] == [product["name"] for product in all_products]

    for product in all_products:
        assert isinstance(product, dict)
        assert expected_keys.issubset(product.keys())

        for key, expected_type in expected_types.items():
            assert isinstance(product[key], expected_type)

def test_get_products_when_empty_database(database):

    all_products = get_all_products(database)

    assert all_products == []

       
def test_add_product(database):
   
    product = {
        "name": "Sok jabłkowy",
        "quantity": 1.5,
        "unit": "l",
        "expiry_date": "2027-04-13"
        }

    add_product(product, database)

    all_products = get_all_products(database)

    product_with_id = {key: value for key, value in all_products[0].items() if key != "id"}

    assert len(all_products) == 1
    assert product_with_id == product

def test_add_product_without_name(database):

    product = {
        "quantity": 1,
        "unit": "l",
        "expiry_date": "2027-04-13"
        }

    with pytest.raises(KeyError):
        add_product(product, database)

def test_add_product_with_invalid_name_type(database):

    product = {
            "name": 123,
            "quantity": 1,
            "unit": "l",
            "expiry_date": "2027-04-13"
            }
    
    with pytest.raises(TypeError):
        add_product(product, database)

def test_add_product_with_empty_name(database):

    product = {
            "name": "",
            "quantity": 1,
            "unit": "l",
            "expiry_date": "2027-04-13"
            }
        
    with pytest.raises(ValueError):
        add_product(product, database)

def test_add_product_with_whitespace_name(database):

    product = {
            "name": "  ",
            "quantity": 1,
            "unit": "l",
            "expiry_date": "2027-04-13"
            }
     
    with pytest.raises(ValueError):
        add_product(product, database)

def test_add_product_quantity_type_int(database):

    product = {
        "name": "Mleko",
        "quantity": 1,
        "unit": "l",
        "expiry_date": "2027-04-13"
        }

    add_product(product, database)
    products = get_all_products(database)

    assert products[-1]["quantity"] ==  1
       
      

def test_add_product_quantity_0(database):

    product = {
        "name": "Mleko",
        "quantity": 0,
        "unit": "l",
        "expiry_date": "2027-04-13"
        }

    with pytest.raises(ValueError):
        add_product(product, database)       
       
def test_add_product_without_quantity(database):

    product = {
        "name": "Mleko",
        "unit": "l",
        "expiry_date": "2027-04-13"
        }
        
    with pytest.raises(KeyError):
        add_product(product, database)   

def test_add_product_with_boolean_quantity(database):

    product = {
        "name": "Mleko",
        "quantity": True,
        "unit": "l",
        "expiry_date": "2027-04-13"
        }

    with pytest.raises(TypeError):
        add_product(product, database) 

    
def test_add_product_with_str_quantity(database): 

    product = {
        "name": "Mleko",
        "quantity": "abc",
        "unit": "l",
        "expiry_date": "2027-04-13"
         }
    
    with pytest.raises(TypeError):
        add_product(product, database) 

def test_add_product_with_negative_quantity(database): 

    product = {
        "name": "Mleko",
        "quantity": -1,
        "unit": "l",
        "expiry_date": "2027-04-13"
        }
        
    with pytest.raises(ValueError):
        add_product(product, database) 


def test_add_product_with_invalid_decimal_precision(database):

    product = {
        "name": "Mleko",
        "quantity": 1.23,
        "unit": "l",
        "expiry_date": "2027-04-13"
         }
            
    with pytest.raises(ValueError):
        add_product(product, database) 


def test_add_product_without_expiry_date(database):

    product = {
        "name": "Mleko",
        "quantity": 1,
        "unit": "l"
        }

    with pytest.raises(KeyError):
        add_product(product, database)

def test_add_product_with_invalid_expiry_date_type(database):

    product = {
        "name": "Mleko",
        "quantity": 1,
        "unit": "l",
        "expiry_date": 123
        }
    
    with pytest.raises(TypeError):
        add_product(product, database)

def test_add_product_with_invalid_expiry_date_format(database):

    product = {
        "name": "Mleko",
        "quantity": 1,
        "unit": "l",
        "expiry_date": "abc"
        }
        
    with pytest.raises(ValueError):
        add_product(product, database)


def test_add_product_with_invalid_expiry_date_from_past(database):

    product = {
        "name": "Mleko",
        "quantity": 1,
        "unit": "l",
        "expiry_date": (date.today() - timedelta(days=1)).isoformat()
        }
        
    with pytest.raises(ValueError):
        add_product(product, database)

def test_add_product_with_expiry_date_current(database):

    product = {
        "name": "Mleko",
        "quantity": 1,
        "unit": "l",
        "expiry_date": date.today().isoformat()
        }
    add_product(product, database)
    saved_products = get_all_products(database)

    assert saved_products[0]["expiry_date"] == product["expiry_date"]


def test_add_product_with_expiry_date_for_future(database):

    product = {
        "name": "Mleko",
        "quantity": 1,
        "unit": "l",
        "expiry_date": "2028-09-09"
        }
    add_product(product, database)
    saved_products = get_all_products(database)

    assert saved_products[0]["expiry_date"] == product["expiry_date"]


# Verify unit validation for different invalid inputs.
@pytest.mark.parametrize("unit, expected_error, include_unit",
                         [
                         (123, TypeError, True),
                         ("", ValueError, True),
                         ("  ", ValueError, True),
                         (None, KeyError, False)
                         ])

def test_add_product_with_invalid_unit(unit, expected_error, include_unit, database):

    product = {
        "name": "Mleko",
        "quantity": 1,
        "expiry_date": "2028-09-09"
        }

    if include_unit:
        product["unit"] = unit

    with pytest.raises(expected_error):
        add_product(product, database)

        

