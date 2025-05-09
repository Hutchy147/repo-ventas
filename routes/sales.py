from flask import Blueprint, request, jsonify
from models.sale import Sale, SaleDetail
from models.client import Client
from models.product import Product
from database import db
from datetime import datetime

sales_bp = Blueprint("sales_bp", __name__)

# Ruta para registrar una venta (POST)
@sales_bp.route("/sales", methods=["POST"])
def register_sale():
    data = request.get_json()

    # Crear la venta principal
    sale = Sale(
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        client_id=data["client_id"],
        discount=data["discount"],
        total=data["total"]
    )
    db.session.add(sale)
    db.session.flush()  # Obtener sale.id antes del commit

    # Registrar los detalles de la venta
    for item in data["details"]:
        detail = SaleDetail(
            sale_id=sale.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            subtotal=item["subtotal"]
        )
        db.session.add(detail)

        # Actualizar el stock del producto
        product = Product.query.get(item["product_id"])
        if product:
            product.stock -= item["quantity"]

    db.session.commit()
    
    return jsonify({"message": "Venta registrada con éxito"}), 201

# Ruta para obtener todas las ventas (GET)
@sales_bp.route("/", methods=["GET"])
def get_sales():
    sales = Sale.query.all()
    result = []
    for sale in sales:
        result.append(sale.sales_invoice())  # Usando el método sales_invoice() para convertir la venta a diccionario
    return jsonify(result), 200

# Ruta para obtener los detalles de todas las ventas (GET)
@sales_bp.route("/details", methods=["GET"])
def get_sale_details():
    details = SaleDetail.query.all()
    result = []
    for detail in details:
        result.append(detail.detail_sale())  # Usando el método detail_sale() para convertir el detalle a diccionario
    return jsonify(result), 200

# Ruta para eliminar una venta y restaurar el stock de los productos (DELETE)
@sales_bp.route("/sales/<int:sale_id>", methods=["DELETE"])
def delete_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"error": "Venta no encontrada"}), 404

    try:
        # Obtenemos los detalles de la venta para actualizar el stock
        details = SaleDetail.query.filter_by(sale_id=sale.id).all()

        for detail in details:
            # Obtener el producto y devolverle el stock
            product = Product.query.get(detail.product_id)
            if product:
                product.stock += detail.quantity  # Restauramos el stock

        # Eliminar los detalles de la venta
        for detail in details:
            db.session.delete(detail)

        # Eliminar la venta
        db.session.delete(sale)
        db.session.commit()

        return jsonify({"message": "Venta eliminada y stock restaurado exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
