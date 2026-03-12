from flask import Flask, request, jsonify

app = Flask(__name__)


class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}


# Fake database
products = [
    Product("1", "Laptop", 1200),
    Product("2", "Phone", 800),
]


# Function : find product
def find_product(product_id):
    for i, p in enumerate(products):
        if p.id == product_id:
            return p, i
    return None, -1


# GET ALL + CREATE
@app.route("/products", methods=["GET", "POST"])
def products_handler():

    # GET /products
    if request.method == "GET":
        return (
            jsonify({"status": "success", "data": [p.to_dict() for p in products]}),
            200,
        )

    # POST /products
    if request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "Invalid request body"}), 400

        new_product = Product(data["id"], data["name"], data["price"])

        products.append(new_product)

        return jsonify({"status": "success", "data": new_product.to_dict()}), 201


# GET ONE / UPDATE / DELETE
@app.route("/products/<id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def product_by_id_handler(id):

    product, index = find_product(id)

    if product is None:
        return jsonify({"status": "error", "message": "Product not found"}), 404

    # GET /products/{id}
    if request.method == "GET":
        return jsonify({"status": "success", "data": product.to_dict()}), 200

    # PUT
    if request.method == "PUT":
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "Invalid request body"}), 400

        products[index] = Product(id, data["name"], data["price"])

        return jsonify({"status": "success", "data": products[index].to_dict()}), 200

    # PATCH
    if request.method == "PATCH":
        data = request.get_json()

        if "name" in data:
            product.name = data["name"]

        if "price" in data:
            product.price = data["price"]

        return jsonify({"status": "success", "data": product.to_dict()}), 200

    # DELETE
    if request.method == "DELETE":
        products.pop(index)

        return jsonify({"status": "success", "message": "Product deleted"}), 200


if __name__ == "__main__":
    port = 5000
    print(f"Server started at http://localhost:{port}")
    app.run(port=port)
