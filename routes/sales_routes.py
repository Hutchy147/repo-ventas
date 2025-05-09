from flask import Blueprint, request, jsonify
from models.sales import Sale
from extensions import db
from datetime import datetime

sales_bp = Blueprint("sales_bp", __name__)

@sales_bp.route("/register", methods=["POST"])
def register_sale():
    data = request.json

    date = datetime.strptime(data["date"], "%Y-%m-%d")
    client = data["client"]
    discount = data["discount"]
    total = data["total"]

    new_sale = Sale(date, client, discount, total)
    db.session.add(new_sale)
    db.session.commit()

    return jsonify(new_sale.to_dict()), 201

@sales_bp.route("/", methods=["GET"])
def get_sales():
    sales = Sale.query.all()
    return jsonify([sale.to_dict() for sale in sales])
