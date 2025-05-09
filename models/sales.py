from extensions import db

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)#clave foranea
    discount = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

class SaleDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"), nullable=False)#clave forane
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)#clave foranea
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
