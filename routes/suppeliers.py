from flask import Blueprint, request, jsonify
from datetime import datetime
from database import db
from models.suppelier import Suppelier
from models.product import Product
from models.phone import Phone
from models.address import Address

suppelier_bp = Blueprint("suppelier", __name__)

@suppelier_bp.route("/get_suppelier", methods=["GET"])
def get_suppelier():
    suppeliers = Suppelier.query.all()
    return jsonify([s.serialize() for s in suppeliers]), 200

@suppelier_bp.route("/post_suppelier", methods=["POST"])
def post_suppelier():
    data = request.get_json()
    required = ["name", "website", "rut"]
    missing = [k for k in required if k not in data]

    if missing:
        return jsonify({"Error": "Faltan datos", "Faltantes": missing}), 400
    if Suppelier.query.filter_by(rut=data["rut"]).first():
        return jsonify({"Error": "Rut ya registrado"}), 400
    if Suppelier.query.filter_by(website=data["website"]).first():
        return jsonify({"Error": "Website ya registrado"}), 400

    try:
        new_suppelier = Suppelier(
            name=data["name"],
            website=data["website"],
            rut=data["rut"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_suppelier)
        db.session.flush()

        for number in data.get("phones", []):
            db.session.add(Phone(number=number, suppelier_id=new_suppelier.id))

        if "address" in data:
            addr = data["address"]
            db.session.add(Address(
                street=addr["street"],
                number=addr["number"],
                apartment=addr.get("apartment"),
                district=addr["district"],
                suppelier_id=new_suppelier.id
            ))

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
        supp.website = data.get("website", supp.website)
        supp.rut = data.get("rut", supp.rut)
        supp.updated_at = datetime.utcnow()

        if "address" in data:
            addr = data["address"]
            if supp.address:
                supp.address.street = addr.get("street", supp.address.street)
                supp.address.number = addr.get("number", supp.address.number)
                supp.address.apartment = addr.get("apartment", supp.address.apartment)
                supp.address.district = addr.get("district", supp.address.district)
            else:
                supp.address = Address(
                    street=addr["street"],
                    number=addr["number"],
                    apartment=addr["apartment"],
                    district=addr["district"],
                    suppelier=supp
                )

        if "phones" in data:
            supp.phones.clear()
            for phone_number in data["phones"]:
                supp.phones.append(Phone(number=phone_number))

        db.session.commit()
        return jsonify({"Mensaje": "Proveedor actualizado"}), 200

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
        if "website" in data: supp.website = data["website"]
        if "rut" in data: supp.rut = data["rut"]
        supp.updated_at = datetime.utcnow()

        if "address" in data:
            addr = data["address"]
            if supp.address:
                supp.address.street = addr.get("street", supp.address.street)
                supp.address.number = addr.get("number", supp.address.number)
                supp.address.apartment = addr.get("apartment", supp.address.apartment)
                supp.address.district = addr.get("district", supp.address.district)
            else:
                supp.address = Address(
                    street=addr["street"],
                    number=addr["number"],
                    apartment=addr.get("apartment"),
                    district=addr["district"],
                    suppelier=supp
                )

        if "phones" in data:
            supp.phones.clear()
            for phone_number in data["phones"]:
                supp.phones.append(Phone(number=phone_number))

        db.session.commit()
        return jsonify({"Mensaje": "Proveedor actualizado"}), 200

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

# Proveedor modifica el stock de su producto
@suppelier_bp.route("/<int:suppelier_id>/product/<int:product_id>/stock", methods=["PUT"])
def update_product_stock_by_suppelier(suppelier_id, product_id):
    data = request.get_json()
    operacion = data.get("operacion")
    cantidad = data.get("cantidad")

    if not operacion or not isinstance(cantidad, int):
        return jsonify({"error": "Datos inválidos"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    if product.suppelier_id != suppelier_id:
        return jsonify({"error": "Este producto no pertenece a este proveedor"}), 403

    try:
        if operacion == "sumar":
            product.stock += cantidad
        elif operacion == "restar":
            if product.stock < cantidad:
                return jsonify({"error": "Stock insuficiente"}), 400
            product.stock -= cantidad
        else:
            return jsonify({"error": "Operación inválida"}), 400

        product.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Stock actualizado", "nuevo_stock": product.stock}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
