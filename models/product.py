from extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, default=0)

    def __init__(self, nombre, marca, stock=0):
        self.nombre = nombre
        self.marca = marca
        self.stock = stock

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "marca": self.marca,
            "stock": self.stock
        }