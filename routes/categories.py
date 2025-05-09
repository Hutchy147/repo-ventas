from flask import Blueprint, request, jsonify
from database import db
from models.category import Category

categories_bp = Blueprint("categories", __name__)

@categories_bp.route("/get_categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200

@categories_bp.route("/create_category", methods=["POST"])
def create_category():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"error": "El nombre es obligatorio"}), 400
    try:
        new_category = Category(
            name=data["name"],
            description=data.get("description")
        )
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@categories_bp.route("/update_category/<int:id>", methods=["PUT"])
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Categoría no encontrada"}), 404
    data = request.get_json()
    try:
        category.name = data.get("name", category.name)
        category.description = data.get("description", category.description)
        db.session.commit()
        return jsonify(category.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@categories_bp.route("/delete_category/<int:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Categoría no encontrada"}), 404
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Categoría eliminada correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
