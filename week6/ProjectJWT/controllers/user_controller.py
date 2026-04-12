from flask import Blueprint, request, jsonify, make_response
from services import user_service
from authentication.auth import auth_required
from authentication.blacklistToken import blacklistToken
from authorization.auth import role_required
from data.role_enum import Role
import jwt
import datetime
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

user_bp = Blueprint("user_bp", __name__)


# LOGOUT
@user_bp.route("/logout", methods=["POST"])
@auth_required
def logout():

    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1]

    blacklistToken.add(token)

    return jsonify({"message": "Logged out successfully"})


# LOGIN
@user_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    email = data.get("email")
    password = data.get("password")

    user = user_service.login(email, password)

    if user is None:
        return jsonify({"error": "Invalid credentials"}), 401

    now = datetime.datetime.utcnow()

    # Access token (ngắn hạn)
    access_token = jwt.encode(
        {
            "email": user.email,
            "role": user.role.name,
            "iat": now,
            "exp": now + datetime.timedelta(minutes=15),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    # Refresh token (dài hạn)
    refresh_token = jwt.encode(
        {
            "email": user.email,
            "iat": now,
            "exp": now + datetime.timedelta(days=7),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 900,
        }
    )


# REFRESH
@user_bp.route("/refresh", methods=["POST"])
def refresh():

    data = request.get_json()

    if not data or "refresh_token" not in data:
        return jsonify({"error": "Refresh token required"}), 400

    token = data.get("refresh_token")

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        new_access_token = jwt.encode(
            {
                "email": decoded["email"],
                "role": decoded["role"],
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        return jsonify({"access_token": new_access_token, "expires_in": 900})

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid refresh token"}), 401


# CRUD USER
@user_bp.route("/users", methods=["GET"])
@auth_required
def get_users():

    users = user_service.get_users()

    response = make_response(jsonify([u.to_dict() for u in users]))

    return response


@user_bp.route("/users", methods=["POST"])
@auth_required
@role_required(Role.ADMIN)
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    user = user_service.create_user(data)

    if user is None:
        return jsonify({"error": "User ID already exists"}), 400

    return jsonify(user.to_dict()), 201


@user_bp.route("/users/<id>", methods=["PUT"])
@auth_required
@role_required(Role.ADMIN)
def update_user(id):

    data = request.get_json()

    user = user_service.update_user(id, data)

    if user is None:
        return "", 404

    return jsonify(user.to_dict())


@user_bp.route("/users/<id>", methods=["DELETE"])
@auth_required
@role_required("ADMIN")
def delete_user(id):

    result = user_service.delete_user(id)

    if not result:
        return "", 404

    return "", 204
