from extensions import db
from models.phone import Phone

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    phones = db.relationship("Phone", backref = "client", cascade = "all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "dni": self.dni,
            "phones": [phone.to_dict() for phone in self.phones]
        }