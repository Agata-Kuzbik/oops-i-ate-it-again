import pytest
import os
from database import init_db
from app import app

@pytest.fixture(scope="function")
def database():

    database = "test_inventory.db"

    if os.path.exists(database):
        os.remove(database)

    init_db(database)

    try:
        yield database

    finally:
        os.remove(database)


@pytest.fixture()
def sample_product():
    product = {
        "name": "Sok jabłkowy",
        "quantity": 1,
        "unit": "l",
        "expiry_date": "2027-04-13"
        }
    return product

@pytest.fixture()
def app_database(database):
    original_database = app.config["DATABASE"]
    app.config["DATABASE"] = database

    try:
        yield app
    finally:
        app.config["DATABASE"] = original_database
