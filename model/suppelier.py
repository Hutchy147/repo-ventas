#Entidad Proveedor
from database import db

class Suppelier(db.Model):#crea entidad proveedor
    __tablename__="suppelier"
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=True)
    phone = db.Column(db.String(20),unique=True,nullable=True)
    website = db.Column(db.String(500),unique=True,nullable=True)
    rut = db.Column(db.String(20),unique=True,nullable=True)
    

    def serialize(self):
        return {
            "id":self.id,#Verifico el id de los proveedores 
            "name":self.name,
            "phone":self.phone,
            "website":self.website,
            "rut":self.rut
        }
        
