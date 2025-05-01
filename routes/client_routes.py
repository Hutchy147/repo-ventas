
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
            telefono=data.get("telefono"),
            direccion=data.get("direccion")
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({"message": "Cliente creado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
