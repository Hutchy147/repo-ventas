from flask import Blueprint, request, jsonify
from models.client import Client
from models.phone import Phone
from models.address import Address
from database import db
from datetime import datetime

client_bp = Blueprint("client_bp", __name__)

@client_bp.route("/get_clients", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    return jsonify([c.to_dict() for c in clients]), 200

@client_bp.route("/create_client", methods=["POST"])
def create_client():
    data = request.get_json()
    try:
        new_client = Client(
            name=data["name"],
            email=data["email"],
            dni=data["dni"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_client)
        db.session.flush()

        for number in data.get("phones", []):
            db.session.add(Phone(number=number, client_id=new_client.id))

        address_data = data.get("address")
        if address_data:
            db.session.add(Address(
                street=address_data["street"],
                number=address_data["number"],
                apartment=address_data.get("apartment"),
                district=address_data["district"],
                client_id=new_client.id
            ))

        db.session.commit()
        return jsonify({"message": "Cliente creado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@client_bp.route("/update_client/<int:id>", methods=["PUT"])
def update_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()
    try:
        client.name = data.get("name", client.name)
        client.email = data.get("email", client.email)
        client.dni = data.get("dni", client.dni)
        client.updated_at = datetime.utcnow()

        if "phones" in data:
            Phone.query.filter_by(client_id=client.id).delete()
            for number in data["phones"]:
                db.session.add(Phone(number=number, client_id=client.id))

        address_data = data.get("address")
        if address_data:
            if client.address:
                client.address.street = address_data.get("street", client.address.street)
                client.address.number = address_data.get("number", client.address.number)
                client.address.apartment = address_data.get("apartment", client.address.apartment)
                client.address.district = address_data.get("district", client.address.district)
            else:
                db.session.add(Address(
                    street=address_data["street"],
                    number=address_data["number"],
                    apartment=address_data.get("apartment"),
                    district=address_data["district"],
                    client_id=client.id
                ))

        db.session.commit()
        return jsonify({"message": "Cliente actualizado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@client_bp.route("/delete_client/<int:id>", methods=["DELETE"])
def delete_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"error": "Cliente no encontrado"}), 404

    try:
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": "Cliente eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400