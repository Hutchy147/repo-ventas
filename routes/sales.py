from flask import Blueprint, request, jsonify
from models.sale import Sale, SaleDetail
from models.client import Client
from models.product import Product
from models.category import Category
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
        sale_data = sale.sales_invoice()

        # Obtener información del cliente
        client = Client.query.get(sale.client_id)
        client_info = {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone
        }

        # Obtener los detalles de la venta, incluyendo la categoría y producto
        details = []
        for detail in sale.sale_details:
            product = Product.query.get(detail.product_id)
            category = Category.query.get(product.category_id)  # Asumiendo que la relación entre producto y categoría está bien definida
            details.append({
                "product_name": product.name,
                "product_price": product.price,
                "category_name": category.name,
                "quantity": detail.quantity,
                "subtotal": detail.subtotal
            })

        sale_data.update({
            "client": client_info,
            "details": details
        })

        result.append(sale_data)

    return jsonify(result), 200

# Ruta para obtener los detalles de una venta (GET)
@sales_bp.route("/details/<int:sale_id>", methods=["GET"])
def get_sale_details(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"error": "Venta no encontrada"}), 404

    sale_data = sale.sales_invoice()

    # Obtener información del cliente
    client = Client.query.get(sale.client_id)
    client_info = {
        "id": client.id,
        "name": client.name,
        "email": client.email,
        "phone": client.phone
    }

    # Obtener los detalles de la venta, incluyendo la categoría y producto
    details = []
    for detail in sale.sale_details:
        product = Product.query.get(detail.product_id)
        category = Category.query.get(product.category_id)  # Relación con la categoría
        details.append({
            "product_name": product.name,
            "product_price": product.price,
            "category_name": category.name,
            "quantity": detail.quantity,
            "subtotal": detail.subtotal
        })

    sale_data.update({
        "client": client_info,
        "details": details
    })

    return jsonify(sale_data), 200

# Ruta para actualizar una venta (PUT)
@sales_bp.route("/sales/<int:sale_id>", methods=["PUT"])
def update_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"error": "Venta no encontrada"}), 404

    data = request.get_json()

    # Actualizar la venta principal
    sale.date = datetime.strptime(data["date"], "%Y-%m-%d")
    sale.client_id = data["client_id"]
    sale.discount = data["discount"]
    sale.total = data["total"]

    # Eliminar detalles anteriores y agregar los nuevos detalles
    SaleDetail.query.filter_by(sale_id=sale.id).delete()

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

    return jsonify({"message": "Venta actualizada con éxito"}), 200

# Ruta para eliminar una venta y restaurar el stock de los productos (DELETE)
@sales_bp.route("/sales/<int:sale_id>", methods=["DELETE"])
def delete_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"error": "Venta no encontrada"}), 404

    try:
        # Obtener cliente asociado a la venta
        client = Client.query.get(sale.client_id)

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

        # Devolver la respuesta con la información del cliente
        client_info = {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone
        }

        return jsonify({
            "message": "Venta eliminada y stock restaurado exitosamente",
            "client": client_info
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
