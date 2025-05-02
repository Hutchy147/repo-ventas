from flask import Blueprint, request, jsonify
from models.product import Product
from extensions import db

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
            stock=data.get("stock", 0)
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
