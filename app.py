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
        quantity = request.form["quantity"]

        if quantity.strip() == "":
            raise ValueError("Product quantity is required")

        product={
            "name": request.form["name"], 
            "quantity": float(quantity), 
            "unit": request.form["unit"], 
            "expiry_date": request.form["expiry_date"]}

        add_product(product)
    except ValueError as error:
        flash(str(error))
    else:
        flash("Product added successfully")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)





