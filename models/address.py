from database import db

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    apartment = db.Column(db.String(10), nullable=True)
    district = db.Column(db.String(50), nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False, unique=True)
    client = db.relationship('Client', back_populates='address')

    def to_dict(self):
        return {
            "street": self.street,
            "number": self.number,
            "apartment": self.apartment,
            "district": self.district
        }
