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


# GET users (Cacheable)
@app.route("/users", methods=["GET"])
def get_users():

    response = make_response(jsonify([u.to_dict() for u in users]))

    # Cache for 60 seconds
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


if __name__ == "__main__":
    port = 5000
    print(f"Server running at http://localhost:{port}")
    app.run(port=port)
