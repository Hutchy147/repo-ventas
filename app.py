#APP
from flask import Flask
from database import db
from routes.suppeliers import suppelier
from model.suppelier import Suppelier

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:4810935@localhost/ventas_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(suppelier,url_prefix="/api/suppelier")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)