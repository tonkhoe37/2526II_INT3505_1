from flask import Blueprint, request, jsonify, make_response
from services import user_service

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():

    users = user_service.get_users()

    response = make_response(jsonify([u.to_dict() for u in users]))

    response.headers["Cache-Control"] = "public, max-age=60"

    return response


@user_bp.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    user = user_service.create_user(data)

    return jsonify(user.to_dict()), 201


@user_bp.route("/users/<id>", methods=["PUT"])
def update_user(id):

    data = request.get_json()

    user = user_service.update_user(id, data)

    if user is None:
        return "", 404

    return jsonify(user.to_dict())


@user_bp.route("/users/<id>", methods=["DELETE"])
def delete_user(id):

    result = user_service.delete_user(id)

    if not result:
        return "", 404

    return "", 204
