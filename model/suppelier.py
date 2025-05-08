#Entidad Proveedor
from database import db

class Suppelier(db.Model):
    __tablename__="suppelier"
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=True)
    adress=db.Column(db.String(100),nullable=True)
    phone=db.Column(db.Integer,unique=True,nullable=True)
    website=db.Column(db.String(500),unique=True,nullable=True)
    rut=db.Column(db.Integer,unique=True,nullable=True)

    def __init__(self,name,adress,phone,website,rut):
        self.name=name
        self.adress=adress
        self.phone=phone
        self.website=website
        self.rut=rut
    

    def serialize(self):
        return {
            "name":self.name,
            "adress":self.adress,
            "phone":self.phone,
            "website":self.website,
            "rut":self.rut
        }
        
