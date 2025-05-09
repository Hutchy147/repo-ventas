from data_base import db
class Client(db.Model):
    _tablename_ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dni = db.Column(db.String(8), nullable=False)  # Ajustado a 8 caracteres
    telefono = db.Column(db.String(20), nullable=True)  # Explícito que permite null

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "dni": self.dni,
            "telefono": self.telefono if self.telefono else None  # Manejo explícito de null
        }