# models/sales.py
from extensions import db

class sales(db.Model):
    __tablename__ = 'sale'
    id = db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Date, nullable=False)
    customer = db.Column(db.String(100), nullable=False)
    discount = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

def __init__(self,date,customer,discount, total):
    self.date=date
    self.customer=customer
    self.discount=discount
    self.total=total

def to_dict(self):
    return {
        "id": self.id,
        "date": self.date.isoformat(),
        "customer": self.customer,
        "discount": self.discount,
        "total": self.total
    }
    