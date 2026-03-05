from flask import Flask, jsonify

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


# API endpoint
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify([u.to_dict() for u in users])


if __name__ == "__main__":
    port = 5000
    print(f"Server running at http://localhost:{port}")
    app.run(port=port)
