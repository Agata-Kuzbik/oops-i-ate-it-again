import sqlite3
from datetime import date


def get_connection(database="inventory.db"):
    """Open and return a connection to the SQLite database."""
    connection = sqlite3.connect(database)
    return connection


def init_db(database="inventory.db"):
    """Create the products table if it does not already exist."""
    connection = get_connection(database)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            expiry_date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def reset_database(database):
    """Clear all records from the products table in the specified database."""
    connection = get_connection(database)
    cursor = connection.cursor()
    
    cursor.execute("""
        DELETE FROM products;
        """)
    
    connection.commit()
    connection.close()


def add_product(product, database="inventory.db"):
    """Insert a new product into the database."""
    if "name" not in product:
        raise KeyError("Name is missing")
    if not isinstance(product["name"], str):
        raise TypeError("Invalid type")
    if product["name"].strip() == "":
        raise ValueError("Product name cannot be empty")
    
    if "quantity" not in product:
        raise KeyError("Quantity is missing")
    if isinstance(product["quantity"], bool):
        raise TypeError("Quantity cannot be boolean")
    if not isinstance(product["quantity"], (int, float)):
        raise TypeError("Invalid type")
    if product["quantity"] <= 0:
        raise ValueError("Invalid value. Value should be > 0")
    if not float(product["quantity"] *10).is_integer():
        raise ValueError("Quantity can have at most one decimal place")

    if "unit" not in product:
        raise KeyError("Unit is missing")
    if not isinstance(product["unit"], str):
        raise TypeError("Invalid type")
    if product["unit"].strip() == "":
        raise ValueError("Product unit cannot be empty")

    if "expiry_date" not in product:
        raise KeyError("Expiry date is missing")
    if not isinstance(product["expiry_date"], str):
        raise TypeError("Invalid type")

    
    today= date.today()
    expiry_date = date.fromisoformat(product["expiry_date"])
    if expiry_date < today:
        raise ValueError("Expiry date cannot be in the past.")
    
            
    

    connection = get_connection(database)
    cursor = connection.cursor()

    # Use placeholders to safely pass product values to the SQL query.
    cursor.execute("""
        INSERT INTO products (name, quantity, unit, expiry_date)
        VALUES (?, ?, ?, ?)
    """, (
        product["name"],
        product["quantity"],
        product["unit"],
        product["expiry_date"]
    ))

    connection.commit()
    connection.close()


def get_all_products(database="inventory.db"):
    """Retrieve all products from the database."""
    connection = get_connection(database)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM products
    """)

    products = cursor.fetchall()
    
    products_dict = []

    for product in products:
        # Convert each database row into a dictionary.
        products_dict.append({
            "id": product[0], 
            "name": product[1], 
            "quantity": product[2], 
            "unit": product[3], 
            "expiry_date": product[4]
            })

    connection.close()
    return products_dict

if __name__ == "__main__":
    # Initialize the database when this file is run directly.
    init_db()
    print(get_all_products())

