import jwt
from flask import request, jsonify
from functools import wraps
import os
from week6.ProjectJWT.authentication.blacklistToken import blacklistToken

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")


def auth_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Invalid or missing token"}), 401

        token = auth_header.split(" ")[1]

        # CHECK BLACKLIST
        if token in blacklistToken:
            return jsonify({"error": "Token revoked"}), 401

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            request.user = decoded

            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

    return decorated
