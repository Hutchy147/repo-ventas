from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuración de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mnga2002@localhost/nombre_base_datos'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importar y registrar rutas
    from routes.client_routes import client_bp
    app.register_blueprint(client_bp, url_prefix="/api/clients")

    return app

# Para levantar el servidor
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
