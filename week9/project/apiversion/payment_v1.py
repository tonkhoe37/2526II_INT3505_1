from flask import Blueprint, request, jsonify, make_response

v1_bp = Blueprint("v1", __name__)


@v1_bp.route("/api/v1/payments", methods=["POST"])
def process_payment_v1():

    data = request.json

    amount = data.get("amount")
    currency = data.get("currency")

    response = make_response(
        jsonify(
            {
                "api_version": "v1",
                "status": "success",
                "message": "Payment processed using API v1",
                "amount": amount,
                "currency": currency,
                "warning": "API v1 is deprecated. Please migrate to v2.",
            }
        ),
        200,
    )

    # Deprecation Headers
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "2026-12-31"

    return response
