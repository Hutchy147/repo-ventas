from flask import Flask
from extensions import db
from routes.clients import client_bp
from models.client import Client
from models.phone import Phone

def create_app():
    app = Flask(__name__)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/ventas_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Esto creará todas las tablas de tus modelos importados
        

    app.register_blueprint(client_bp, url_prefix="/api/clients")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)