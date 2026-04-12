from flask import Blueprint, request, jsonify, make_response
from services import user_service


SECRET_KEY = "bc123xyz456"

user_bp = Blueprint("user_bp", __name__)


# GET USERS (3 pagination)
# page_based : http://localhost:5000/users?type=page&page=90000&size=10
# cursor_based : http://localhost:5000/users?type=cursor&last_id=899990&size=10
# offset_based : http://localhost:5000/users?type=offset&offset=899990&size=10
@user_bp.route("/users", methods=["GET"])
def get_all_users():

    type = request.args.get("type", "page")
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    last_id = request.args.get("last_id")
    offset = request.args.get("offset")

    if last_id:
        last_id = int(last_id)

    if offset:
        offset = int(offset)

    try:
        users = user_service.get_users(type, page, size, last_id, offset)
        return jsonify([u.to_dict() for u in users])

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# CREATE USER
@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    user_service.create_user(data)

    return jsonify({"message": "User created"}), 201


# UPDATE USER
@user_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()

    result = user_service.update_user(id, data)

    if not result:
        return "", 404

    return jsonify({"message": "User updated"})


# DELETE USER
@user_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    result = user_service.delete_user(id)

    if not result:
        return "", 404

    return "", 204


"""
@user_bp.route("/users", methods=["GET"])
@auth_required
def get_all_users():

    type = request.args.get("type", "page")
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    last_id = request.args.get("last_id")
    offset = request.args.get("offset")

    if last_id:
        last_id = int(last_id)
    if offset:
        offset = int(offset)

    users, total, total_pages = user_service.get_users_with_meta(
        type, page, size, last_id, offset
    )

    response = {
        "type": type,
        "size": size,
        "data": [u.to_dict() for u in users]
    }

    # chỉ thêm metadata cho page-based
    if type == "page":
        response["page"] = page
        response["total_items"] = total
        response["total_pages"] = total_pages

    return jsonify(response)
"""
