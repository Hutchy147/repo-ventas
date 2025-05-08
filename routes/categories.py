from flask import Blueprint, request, jsonify
from app import db
from models.category import category

category_bp = Blueprint("category",__name__)

@category_bp.route("/categories", methods = ["POST"])
def create_category():
    