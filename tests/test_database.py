from database import get_all_products, add_product
from datetime import datetime, date
import pytest


def test_get_all_products(database, sample_product):

    add_product(sample_product, database)
    all_products = get_all_products(database)
    expected_keys = {"id", "name", "quantity", "unit", "expiry_date"}
    expected_types = {
        "id": int,
        "name": str,
        "quantity": float,
        "unit": str,
        "expiry_date": str,
    }


    assert isinstance(all_products, list)
    assert len(all_products) == 1
    assert all_products[0]["name"] == sample_product["name"]

    for product in all_products:
        assert isinstance(product, dict)
        assert expected_keys.issubset(product.keys())
        assert product["name"].strip() != ""
        assert product["unit"].strip() != ""
        assert product["expiry_date"].strip() != ""
        assert datetime.strptime(product["expiry_date"], "%Y-%m-%d")
        
        for key, expected_type in expected_types.items():
            assert isinstance(product[key], expected_type)

       
def test_add_product(database):
   
    product = {
        "name": "Sok jabłkowy",
        "quantity": 1.5,
        "unit": "l",
        "expiry_date": "2027-04-13"
        }

    add_product(product, database)

    all_products = get_all_products(database)

    assert len(all_products) == 1
    assert all_products[0]["name"] == "Sok jabłkowy"
    assert all_products[0]["quantity"] == 1.5
    assert all_products[0]["unit"] == "l"
    assert all_products[0]["expiry_date"] == "2027-04-13"


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
    assert products[-1]["name"] == "Mleko"
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
        "expiry_date": "2020-01-01"
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
    assert any( saved_product["name"] == product["name"] for saved_product in get_all_products(database))


def test_add_product_with_expiry_date_for_future(database):

    product = {
        "name": "Mleko",
        "quantity": 1,
        "unit": "l",
        "expiry_date": "2028-09-09"
        }
    add_product(product, database)
    assert any( saved_product["name"] == product["name"] for saved_product in get_all_products(database))


# Verify unit validation for different invalid inputs.
@pytest.mark.parametrize("unit, expected_error, include_unit",
                         [
                         (123, TypeError, True),
                         ("", ValueError, True),
                         ("  ", ValueError, True),
                         (None, KeyError, False)
                         ])

def test_add_product_with_invalid_unit(unit, expected_error,include_unit, database):

    product = {
        "name": "Mleko",
        "quantity": 1,
        "expiry_date": "2028-09-09"
        }

    if include_unit:
        product["unit"] = unit

    with pytest.raises(expected_error):
        add_product(product, database)

        

