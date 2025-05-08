#APP
from flask import Flask
from Database import db
from routes.suplier_route import suplier
from model.suplier import Suplier

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEW_DATABASE_URI"] = "mysql+pymysql://root:4810935@localhost/ventas_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(suplier,url_prefix="/api/suplier")

if __name__ == "__main__":
    app=create_app()
    app.run(debug=True)