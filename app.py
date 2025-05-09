from flask import Flask
from config import Config
from data_base import db
from routes.sales import sales_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    app.register_blueprint(sales_bp, url_prefix="/api/sales")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)