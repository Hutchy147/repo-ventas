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
    suppelier_id = db.Column(db.Integer, db.ForeignKey('suppelier.id'), nullable=False)  # Relación con proveedor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones con otros modelos
    sale_details = db.relationship("SaleDetail", back_populates="product", cascade="all, delete-orphan")
    category = db.relationship('Category', back_populates='products')
    suppelier = db.relationship('Suppelier', back_populates='products')

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "marca": self.marca,
            "stock": self.stock,
            "precio_actual": self.precio_actual,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "category": self.category.to_dict() if self.category else None,  # Relación con categoría
            "suppelier": self.suppelier.to_dict() if self.suppelier else None  # Relación con proveedor
        }
