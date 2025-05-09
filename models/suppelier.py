from database import db
from datetime import datetime

class Suppelier(db.Model):
    __tablename__ = "suppelier"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(500), unique=True, nullable=True)
    rut = db.Column(db.String(20), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con productos
    products = db.relationship('Product', back_populates='suppelier')

    # Relación con dirección
    address = db.relationship('Address', back_populates='suppelier', uselist=False, cascade='all, delete-orphan')

    # Relación con teléfonos
    phones = db.relationship('Phone', back_populates='suppelier', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "website": self.website,
            "rut": self.rut,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "address": self.address.to_dict() if self.address else None, # Relación con dirección
            "phones": [p.to_dict() for p in self.phones], # Relación con teléfonos
            "products": [product.to_dict() for product in self.products]  # Relación con productos
        }
