
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from routes.client_routes import client_bp
    app.register_blueprint(client_bp, url_prefix="/api/clients")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
