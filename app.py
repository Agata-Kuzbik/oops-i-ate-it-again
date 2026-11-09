from flask import Flask, jsonify,render_template, request, redirect, url_for, flash
from database import get_all_products, add_product



app = Flask(__name__)
app.secret_key = "dev-secret-key"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/products")
def get_products():
    products = get_all_products()
    return jsonify(products)

@app.route("/products", methods=["POST"])
def add_product_route():
    try:
        quantity = request.form.get("quantity")
        name = request.form.get("name")
        unit = request.form.get("unit")
        expiry_date = request.form.get("expiry_date")

        if not quantity or quantity.strip() == "":
            raise ValueError("Product quantity is required")
        if not name or name.strip() == "":
            raise ValueError("Product name is required")
        if not unit or unit.strip() == "":
            raise ValueError("Product unit is required")
        if not expiry_date or expiry_date.strip() == "":
            raise ValueError("Product expiry date is required")
        
        product={
            "name": name.strip(), 
            "quantity": float(quantity), 
            "unit": unit.strip(), 
            "expiry_date": expiry_date
            }

        add_product(product)
        
    except (ValueError, TypeError) as error:
        flash(str(error))
    else:
        flash("Product added successfully")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)





