#Entidad Proveedor
from database import db
from datetime import datetime

class Suppelier(db.Model):
    _tablename_ = "suppelier"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(500), unique=True, nullable=True)
    rut = db.Column(db.String(20), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    address = db.relationship('Address', back_populates='suppelier', uselist=False, cascade='all, delete-orphan')
    phones = db.relationship('Phone', back_populates='suppelier', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,#verifico el id del proveedor
            "name": self.name,
            "website": self.website,
            "rut": self.rut,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "address": self.address.to_dict() if self.address else None,
            "phones": [p.to_dict() for p in self.phones]
        }
        
