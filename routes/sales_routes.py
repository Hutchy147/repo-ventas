from flask import Blueprint, request, jsonify
from models.sales import Sale, SaleDetail
from extensions import db
from datetime import datetime

sales_bp = Blueprint("sales_bp", __name__)

@sales_bp.route("/sales", methods=["POST"])
def register_sale():
    data = request.get_json()

    sale = Sale(
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        client_id=data["client_id"],
        discount=data["discount"],
        total=data["total"]
    )
    db.session.add(sale)
    db.session.flush()  # Obtener sale.id antes del commit

    for item in data["details"]:
        detail = SaleDetail(
            sale_id=sale.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            subtotal=item["subtotal"]
        )
        db.session.add(detail)

    db.session.commit()
    return jsonify({"message": "Venta registrada con éxito"}), 201

@sales_bp.route("/sales", methods=["GET"])
def get_sales():
    sales = Sale.query.all()
    result = []
    for sale in sales:
        result.append({
            "id": sale.id,
            "date": sale.date.strftime("%Y-%m-%d"),
            "client_id": sale.client_id,
            "total": sale.total,
            "discount": sale.discount
        })
    return jsonify(result)
