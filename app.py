from flask import Flask
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()  # Esto creará todas las tablas de tus modelos importados

    # Importar solo rutas de productos (en esta rama)
    from routes.product_routes import product_bp
    app.register_blueprint(product_bp, url_prefix="/api/products")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
