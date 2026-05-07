from flask import Flask
from apiversion.payment_v1 import v1_bp
from apiversion.payment_v2 import v2_bp

app = Flask(__name__)

# Register APIs
app.register_blueprint(v1_bp)
app.register_blueprint(v2_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
