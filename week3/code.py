from flask import Flask, request, jsonify

app = Flask(__name__)

# CONFIG
API_V1 = "/api/v1"
API_V2 = "/api/v2"


# MODEL
class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def to_dict_v1(self):
        return {"id": self.id, "name": self.name, "price": self.price}

    def to_dict_v2(self):
        return {
            "productId": self.id,
            "productName": self.name,
            "price": self.price,
            "currency": "USD",  # thêm field mới
        }


# ==============================
# FAKE DATABASE
# ==============================
products = [
    Product("1", "Laptop", 1200),
    Product("2", "Phone", 800),
    Product("3", "Tablet", 600),
    Product("4", "Monitor", 300),
]


# UTILS
def success_response(data=None, message="Success", status=200, meta=None):
    return (
        jsonify({"status": "success", "message": message, "data": data, "meta": meta}),
        status,
    )


def error_response(message="Error", status=400):
    return jsonify({"status": "error", "message": message}), status


def validate_product(data, require_all=True):
    if not data:
        return "Request body is required"

    if require_all:
        if "id" not in data:
            return "Missing id"
        if "name" not in data:
            return "Missing name"
        if "price" not in data:
            return "Missing price"

    return None


# SERVICE
def find_product(product_id):
    for i, p in enumerate(products):
        if p.id == product_id:
            return p, i
    return None, -1


def is_duplicate_id(product_id):
    product, _ = find_product(product_id)
    return product is not None


# V1 ROUTES (GIỮ NGUYÊN)
@app.route(f"{API_V1}/products", methods=["GET", "POST"])
def products_v1():

    if request.method == "GET":
        return success_response([p.to_dict_v1() for p in products])

    if request.method == "POST":
        data = request.get_json()

        error = validate_product(data)
        if error:
            return error_response(error)

        if is_duplicate_id(data["id"]):
            return error_response("Product ID already exists", 409)

        new_product = Product(data["id"], data["name"], data["price"])
        products.append(new_product)

        return success_response(new_product.to_dict_v1(), "Created", 201)


@app.route(f"{API_V1}/products/<id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def product_v1(id):

    product, index = find_product(id)

    if product is None:
        return error_response("Product not found", 404)

    if request.method == "GET":
        return success_response(product.to_dict_v1())

    if request.method == "PUT":
        data = request.get_json()

        error = validate_product(data)
        if error:
            return error_response(error)

        products[index] = Product(id, data["name"], data["price"])
        return success_response(products[index].to_dict_v1(), "Updated")

    if request.method == "PATCH":
        data = request.get_json()

        if "name" in data:
            product.name = data["name"]
        if "price" in data:
            product.price = data["price"]

        return success_response(product.to_dict_v1(), "Updated")

    if request.method == "DELETE":
        products.pop(index)
        return success_response(message="Deleted")


# V2 ROUTES (NÂNG CẤP)
@app.route(f"{API_V2}/products", methods=["GET"])
def products_v2():

    # Pagination
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 2))

    start = (page - 1) * limit
    end = start + limit

    paginated = products[start:end]

    data = [p.to_dict_v2() for p in paginated]

    meta = {"page": page, "limit": limit, "total": len(products)}

    return success_response(data, meta=meta)


@app.route(f"{API_V2}/products/<id>", methods=["GET"])
def product_v2(id):

    product, _ = find_product(id)

    if product is None:
        return error_response("Product not found", 404)

    return success_response(product.to_dict_v2())


# GLOBAL ERROR
@app.errorhandler(500)
def internal_error(e):
    return error_response("Internal Server Error", 500)


# RUN
if __name__ == "__main__":
    port = 5000
    print(f"Server running at http://localhost:{port}")
    app.run(port=port)
