from extensions import db

class Phone(db.Model):
    __tablename__ = "phones"

    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.String(30), nullable = False)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number
        }