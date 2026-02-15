from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from src.config.env import Config

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Config.SECRET_KEY

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # register blueprints - todavia no existen

    # Init SocketIO with CORS
    socketio.init_app(app, cors_allowed_origins="*")

    @app.route("/")
    def health():
        return {"status": "online", "message": "Lummia Platform API", "version": "2.1.0"}, 200

    return app

if __name__ == "__main__":
    Config.validate()
    app = create_app()
    print(f"\n{'='*45}")
    print(f" LUMMIA PLATFORM API v2.1.0")
    print(f" http://localhost:{Config.PORT}")
    print(f" WebSocket enabled")
    print(f"{'='*45}\n")
    socketio.run(app, host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG, allow_unsafe_werkzeug=True)