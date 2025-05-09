from flask import Blueprint, request, jsonify
from models.product import Product
from database import db
from datetime import datetime

product_bp = Blueprint("product_bp", __name__)

@product_bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

@product_bp.route("/", methods=["POST"])
def create_product():
    data = request.get_json()
    try:
        new_product = Product(
            nombre=data["nombre"],
            marca=data["marca"],
            stock=data.get("stock", 0),
            precio_actual=data.get("precio_actual", 0.0),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Producto creado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@product_bp.route("/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.get_json()
    try:
        product.nombre = data.get("nombre", product.nombre)
        product.marca = data.get("marca", product.marca)
        product.stock = data.get("stock", product.stock)
        product.precio_actual = data.get("precio_actual", product.precio_actual)
        product.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({"message": "Producto actualizado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@product_bp.route("/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Producto eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@product_bp.route("/<int:id>/stock", methods=["PUT"])
def modificar_stock(id):
    data = request.get_json()
    operacion = data.get("operacion")
    cantidad = data.get("cantidad")

    if not operacion or not isinstance(cantidad, int):
        return jsonify({"error": "Datos inválidos"}), 400

    producto = Product.query.get(id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    try:
        if operacion == "sumar":
            producto.stock += cantidad
        elif operacion == "restar":
            if producto.stock < cantidad:
                return jsonify({"error": "Stock insuficiente"}), 400
            producto.stock -= cantidad
        else:
            return jsonify({"error": "Operación no válida"}), 400

        producto.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"mensaje": "Stock actualizado", "nuevo_stock": producto.stock}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@product_bp.route("/<int:id>/precio", methods=["PUT"])
def modificar_precio(id):
    data = request.get_json()
    nuevo_precio = data.get("precio_actual")

    if nuevo_precio is None or not isinstance(nuevo_precio, (int, float)):
        return jsonify({"error": "Precio inválido"}), 400

    producto = Product.query.get(id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    try:
        producto.precio_actual = nuevo_precio
        producto.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"mensaje": "Precio actualizado", "nuevo_precio": producto.precio_actual}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500