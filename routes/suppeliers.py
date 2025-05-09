from flask import Blueprint, request, jsonify
from models.suppelier import Suppelier
from models.product import Product
from database import db
from datetime import datetime

suppelier_bp = Blueprint("suppelier", __name__)

@suppelier_bp.route("/get_suppelier", methods=["GET"])
def get_suppelier():
    suppeliers = Suppelier.query.all()
    return jsonify([s.serialize() for s in suppeliers]), 200

@suppelier_bp.route("/post_suppelier", methods=["POST"])
def post_suppelier():
    data = request.get_json()
    required = ["name", "phone", "website", "rut"]
    missing = [k for k in required if k not in data]

    if missing:
        return jsonify({"Error": "Faltan datos", "Faltantes": missing}), 400
    if Suppelier.query.filter_by(rut=data["rut"]).first():
        return jsonify({"Error": "Rut ya registrado"}), 400
    if Suppelier.query.filter_by(phone=data["phone"]).first():
        return jsonify({"Error": "Teléfono ya registrado"}), 400
    if Suppelier.query.filter_by(website=data["website"]).first():
        return jsonify({"Error": "Website ya registrado"}), 400

    try:
        new_suppelier = Suppelier(
            name=data["name"],
            phone=data["phone"],
            website=data["website"],
            rut=data["rut"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_suppelier)
        db.session.commit()
        return jsonify(new_suppelier.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500

@suppelier_bp.route("/put_suppelier/<int:id>", methods=["PUT"])
def put_suppelier(id):
    supp = Suppelier.query.get(id)
    if not supp:
        return jsonify({"Mensaje": "Proveedor no encontrado"}), 404

    data = request.get_json()
    try:
        supp.name = data.get("name", supp.name)
        supp.phone = data.get("phone", supp.phone)
        supp.website = data.get("website", supp.website)
        supp.rut = data.get("rut", supp.rut)
        supp.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({"Mensaje": "Proveedor actualizado"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500

@suppelier_bp.route("/patch_suppelier/<int:id>", methods=["PATCH"])
def patch_suppelier(id):
    supp = Suppelier.query.get(id)
    if not supp:
        return jsonify({"Mensaje": "Proveedor no encontrado"}), 404

    data = request.get_json()
    try:
        if "name" in data: supp.name = data["name"]
        if "phone" in data: supp.phone = data["phone"]
        if "website" in data: supp.website = data["website"]
        if "rut" in data: supp.rut = data["rut"]
        supp.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({"Mensaje": "Proveedor actualizado"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500

@suppelier_bp.route("/delete_suppelier/<int:id>", methods=["DELETE"])
def delete_suppelier(id):
    supp = Suppelier.query.get(id)
    if not supp:
        return jsonify({"Mensaje": "No se encuentra proveedor"}), 404

    try:
        db.session.delete(supp)
        db.session.commit()
        return jsonify({"Mensaje": "Proveedor eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500

# Ruta nueva: proveedor actualiza stock de un producto
@suppelier_bp.route("/<int:suppelier_id>/product/<int:product_id>/stock", methods=["PUT"])
def update_product_stock_by_suppelier(suppelier_id, product_id):
    data = request.get_json()
    operacion = data.get("operacion")
    cantidad = data.get("cantidad")

    if not operacion or not isinstance(cantidad, int):
        return jsonify({"error": "Invalid data"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if product.suppelier_id != suppelier_id:
        return jsonify({"error": "Product does not belong to the supplier"}), 403

    try:
        if operacion == "sumar":
            product.stock += cantidad
        elif operacion == "restar":
            if product.stock < cantidad:
                return jsonify({"error": "Insufficient stock"}), 400
            product.stock -= cantidad
        else:
            return jsonify({"error": "Invalid operation"}), 400

        product.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Stock updated", "new_stock": product.stock}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
