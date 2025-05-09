from flask import Flask
from database import db
from routes.clients import client_bp
from routes.products import product_bp
from routes.suppeliers import suppelier_bp
from routes.categories import categories_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/ventas_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Blueprints
    app.register_blueprint(client_bp, url_prefix="/api/clients")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(suppelier_bp, url_prefix="/api/suppeliers")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
