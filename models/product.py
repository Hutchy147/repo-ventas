from database import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, default=0)
    precio_actual = db.Column(db.Float, nullable=False, default=0.0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship('Category', back_populates='products')

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "marca": self.marca,
            "stock": self.stock,
            "precio_actual": self.precio_actual,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
