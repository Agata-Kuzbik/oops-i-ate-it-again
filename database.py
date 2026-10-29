import sqlite3


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
            quantity INTEGER NOT NULL,
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

