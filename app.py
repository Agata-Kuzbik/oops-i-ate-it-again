from flask import Flask, jsonify
from database import get_all_products

app = Flask(__name__)

@app.route("/")
def home():
    return "Oops! I Ate It Again!"

@app.route("/api/products")
def products():
    products = get_all_products()
    return jsonify(products)



if __name__ == "__main__":
    app.run(debug=True)





