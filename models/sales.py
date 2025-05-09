from extensions import db

class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    client = db.Column(db.String(100), nullable=False)
    discount = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def __init__(self, date, client, discount, total):
        self.date = date
        self.client = client
        self.discount = discount
        self.total = total

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "client": self.client,
            "discount": self.discount,
            "total": self.total
        }
