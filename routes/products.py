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
    required_fields = ["nombre", "marca", "category_id", "suppelier_id"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": "Missing required fields", "fields": missing_fields}), 400

    # Validación básica: valores por defecto para opcionales
    stock = data.get("stock", 0)
    precio_actual = data.get("precio_actual", 0.0)

    # Validar que category_id y suppelier_id existan
    from models.category import Category
    from models.suppelier import Suppelier

    category = Category.query.get(data["category_id"])
    suppelier = Suppelier.query.get(data["suppelier_id"])

    if not category:
        return jsonify({"error": "Category not found"}), 404
    if not suppelier:
        return jsonify({"error": "Suppelier not found"}), 404

    try:
        new_product = Product(
            nombre=data["nombre"],
            marca=data["marca"],
            stock=stock,
            precio_actual=precio_actual,
            category_id=data["category_id"],
            suppelier_id=data["suppelier_id"],
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

# Route to update stock by the supplier
@product_bp.route("/<int:id>/stock", methods=["PUT"])
def update_stock_by_supplier(id):
    data = request.get_json()
    operation = data.get("operation")
    quantity = data.get("quantity")

    if not operation or not isinstance(quantity, int):
        return jsonify({"error": "Datos inválidos"}), 400

    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    try:
        if operation == "add":
            product.stock += quantity
        elif operation == "subtract":
            if product.stock < quantity:
                return jsonify({"error": "Stock insuficiente"}), 400
            product.stock -= quantity
        else:
            return jsonify({"error": "Operación no válida"}), 400

        product.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Stock actualizado", "nuevo_stock": product.stock}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@product_bp.route("/<int:id>/price", methods=["PUT"])
def modify_price(id):
    data = request.get_json()
    new_price = data.get("precio_actual")

    if new_price is None or not isinstance(new_price, (int, float)):
        return jsonify({"error": "Precio inválido"}), 400

    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    try:
        product.precio_actual = new_price
        product.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Precio actualizado", "nuevo_precio": product.precio_actual}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
