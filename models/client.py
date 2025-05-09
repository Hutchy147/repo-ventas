from database import db
from datetime import datetime

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con la dirección, un solo cliente tiene una dirección
    address = db.relationship('Address', back_populates='client', uselist=False, cascade='all, delete-orphan')

    # Relación con los teléfonos, un cliente puede tener varios números de teléfono
    phones = db.relationship('Phone', back_populates='client', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "dni": self.dni,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "phones": [phone.to_dict() for phone in self.phones],  # Devuelve los teléfonos asociados al cliente
            "address": self.address.to_dict() if self.address else None  # Devuelve la dirección si existe
            }