from app import db

class category(db.model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(250), nullable = True)

    products = db.relationship("Produc", beckref="Category", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }