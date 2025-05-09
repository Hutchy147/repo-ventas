from database import db
from datetime import datetime

class Phone(db.Model):
    __tablename__ = "phones"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(30), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    suppelier_id = db.Column(db.Integer, db.ForeignKey('suppelier.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = db.relationship('Client', back_populates='phones')
    suppelier = db.relationship('Suppelier', back_populates='phones')

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
