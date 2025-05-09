from database import db
from datetime import datetime

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    street_number = db.Column(db.String(10), nullable=False)
    apartment = db.Column(db.String(10), nullable=True)
    district = db.Column(db.String(50), nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = db.relationship('Client', back_populates='address')
    supplier = db.relationship('Supplier', back_populates='address')

    def to_dict(self):
        return {
            "id": self.id,
            "street": self.street,
            "street_number": self.street_number,
            "apartment": self.apartment,
            "district": self.district,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
