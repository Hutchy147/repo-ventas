from database import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(250), nullable = True)

    #products = db.relationship("Produc", beckref="Category", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }