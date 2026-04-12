from flask import Flask
from controllers.user_controller import user_bp

app = Flask(__name__)

app.register_blueprint(user_bp)

if __name__ == "__main__":
    port = 5000
    print(f"Server running at http://localhost:{port}")
    app.run(port=port)
