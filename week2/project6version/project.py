from flask import Flask, request, jsonify, make_response

app = Flask(__name__)


class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


# Fake database
users = [
    User("1", "Ton Thien Khoe", "khoe@gmail.com"),
    User("2", "Nguyen Van A", "vana@gmail.com"),
]


# GET users (cacheable)
@app.route("/users", methods=["GET"])
def get_users():

    response = make_response(jsonify([u.to_dict() for u in users]))

    response.headers["Cache-Control"] = "public, max-age=60"

    return response


# POST create user
@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    new_user = User(data["id"], data["name"], data["email"])

    users.append(new_user)

    return jsonify(new_user.to_dict()), 201


# PUT update full user
@app.route("/users/<id>", methods=["PUT"])
def update_user(id):

    data = request.get_json()

    if not data:
        return "", 400

    for i, u in enumerate(users):
        if u.id == id:
            users[i] = User(id, data["name"], data["email"])
            return jsonify(users[i].to_dict()), 200

    return "", 404


# PATCH update partial user
@app.route("/users/<id>", methods=["PATCH"])
def patch_user(id):

    data = request.get_json()

    if not data:
        return "", 400

    for u in users:

        if u.id == id:

            if "name" in data:
                u.name = data["name"]

            if "email" in data:
                u.email = data["email"]

            return jsonify(u.to_dict()), 200

    return "", 404


# DELETE user
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):

    for i, u in enumerate(users):
        if u.id == id:
            users.pop(i)
            return "", 204

    return "", 404


if __name__ == "__main__":
    port = 5000
    print(f"Server running at http://localhost:{port}")
    app.run(port=port)
