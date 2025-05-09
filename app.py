from config import Config
from database import db
from models.category import Category


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        from models.category import Category 
        db.create_all()  # Esto creará todas las tablas de tus modelos importados

    # Importar solo rutas de productos (en esta rama)
    from routes.categories import category_bp
    app.register_blueprint(category_bp, url_prefix="/api/categories")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)