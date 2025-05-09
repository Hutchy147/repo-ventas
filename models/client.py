from extensions import db
from models.phone import Phone

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    
    address = db.relationship('Address', uselist=False, back_populates='client', cascade='all, delete')
    phones = db.relationship("Phone", backref = "client", cascade = "all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "dni": self.dni,
            "phones": [phone.to_dict() for phone in self.phones],
            "address": self.address.to_dict() if self.address else None
        }