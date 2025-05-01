from flask import Flask
from extensions import db  
from routes.client_routes import client_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mnga2002@localhost/ventas_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(client_bp, url_prefix="/api/clients")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
