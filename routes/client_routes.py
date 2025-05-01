
from flask import Blueprint, request, jsonify
from models.client import Client
from app import db

client_bp = Blueprint("client_bp", __name__)

@client_bp.route("/", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    return jsonify([c.to_dict() for c in clients]), 200

@client_bp.route("/", methods=["POST"])
def create_client():
    data = request.get_json()
    try:
        new_client = Client(
            nombre=data["nombre"],
            email=data["email"],
            dni=data["dni"],
            telefono=data.get("telefono")
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({"message": "Cliente creado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@client_bp.route("/<int:id>", methods=["PUT"])
def update_client(id):
    data = request.get_json()
    client = Client.query.get(id)

    if not client:
        return jsonify({"error": "Cliente no encontrado"}), 404

    try:
        client.nombre = data.get("nombre", client.nombre)
        client.email = data.get("email", client.email)
        client.dni = data.get("dni", client.dni)
        client.telefono = data.get("telefono", client.telefono)

        db.session.commit()
        return jsonify({"message": "Cliente actualizado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@client_bp.route("/<int:id>", methods=["DELETE"])
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
