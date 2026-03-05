from flask import Flask, request, jsonify

app = Flask(__name__)


class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


# database
users = [
    User("1", "Ton THien Khoe", "khoe@gmail.com"),
    User("2", "Nguyen Van A", "vanA@gmail.com"),
]


# endpoint /users
@app.route("/users", methods=["GET", "POST"])
def users_handler():

    if request.method == "GET":
        return jsonify([u.to_dict() for u in users]), 200

    if request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid data"}), 400

        new_user = User(data["id"], data["name"], data["email"])
        users.append(new_user)

        return jsonify(new_user.to_dict()), 201


# endpoint /users/{id}
@app.route("/users/<id>", methods=["PUT", "PATCH", "DELETE"])
def users_by_id_handler(id):

    user = None
    index = -1

    for i, u in enumerate(users):
        if u.id == id:
            user = u
            index = i
            break

    if user is None:
        return "", 404

    if request.method == "PUT":
        data = request.get_json()

        if not data:
            return "", 400

        users[index] = User(id, data["name"], data["email"])

        return jsonify(users[index].to_dict()), 200

    if request.method == "PATCH":
        data = request.get_json()

        if not data:
            return "", 400

        if "name" in data:
            user.name = data["name"]

        if "email" in data:
            user.email = data["email"]

        return jsonify(user.to_dict()), 200

    if request.method == "DELETE":
        users.pop(index)
        return "", 204


if __name__ == "__main__":
    port = 5000
    print(f"Server started at http://localhost:{port}")
    app.run(port=port)

# Get curl "http://localhost:5000/users"
# Post curl -X POST -H "Content-Type: application/json" -d '{"id": "3", "name": "Nguyen Van B", "email": "
# Delete curl -X DELETE "http://localhost:5000/users/3"
# Put curl -X PUT -H "Content-Type: application/json" -d '{"name": "Nguyen Van C", "email": "
# Patch curl -X PATCH -H "Content-Type: application/json" -d '{"name": "Nguyen Van D"}' "http://localhost:5000/users/2"
