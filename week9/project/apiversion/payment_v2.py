from flask import Blueprint, request, jsonify

v2_bp = Blueprint("v2", __name__)


@v2_bp.route("/api/v2/payments", methods=["POST"])
def process_payment_v2():

    data = request.json

    amount = data.get("amount")
    currency = data.get("currency")
    payment_method = data.get("payment_method")
    token = data.get("token")

    # Validation
    if not all([amount, currency, payment_method, token]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    return (
        jsonify(
            {
                "api_version": "v2",
                "status": "success",
                "message": "Payment processed using API v2",
                "transaction_id": "TXN-999999",
                "payment_method": payment_method,
            }
        ),
        200,
    )
