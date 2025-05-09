from data_base import db

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)  # clave foránea
    discount = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    # Método para convertir la venta a un diccionario
    def sales_invoice(self):
        return {
            "id": self.id,
            "date": self.date,
            "client_id": self.client_id,
            "discount": self.discount,
            "total": self.total
        }

class SaleDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"), nullable=False)  # clave foránea
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)  # clave foránea
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    # Método para convertir el detalle de la venta a un diccionario
    def detail_sale(self):
        return {
            "id": self.id,
            "sale_id": self.sale_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "subtotal": self.subtotal
        }
