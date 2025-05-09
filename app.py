from flask import Flask
from config import Config
from database import db
from models.category import Category

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from models.product import Product  
        db.create_all()

    from routes.product_routes import product_bp
    app.register_blueprint(product_bp, url_prefix="/api/products")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)