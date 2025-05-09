#seed

from database import db
from app import app
from models.client import Client
from models.suppelier import Suppelier
from models.product import Product
from models.category import Category
from models.phone import Phone
from models.address import Address
from models.sale import Sale, SaleDetail
from datetime import datetime
import json

with app.app_context():
    try:
        # Cargar clientes
        with open("data_json/clients.json", encoding="utf-8") as file:
            clients_data = json.load(file)
            for client in clients_data:
                if not Client.query.filter_by(email=client["email"]).first():
                    new_client = Client(
                        name=client["name"],
                        email=client["email"],
                        dni=client["dni"],
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(new_client)
                    db.session.flush()

                    for number in client.get("phones", []):
                        db.session.add(Phone(number=number, client_id=new_client.id))

                    address_data = client.get("address")
                    if address_data:
                        db.session.add(Address(
                            street=address_data["street"],
                            street_number=address_data["number"],
                            apartment=address_data.get("apartment"),
                            district=address_data["district"],
                            client_id=new_client.id
                        ))
            db.session.commit()
            print("Clientes cargados")

        # Cargar categorías
        with open("data_json/categories.json", encoding="utf-8") as file:
            categories = json.load(file)
            for cat in categories:
                if not Category.query.filter_by(name=cat["name"]).first():
                    db.session.add(Category(name=cat["name"]))
            db.session.commit()

        # Cargar proveedores
        with open("data_json/suppeliers.json", encoding="utf-8") as file:
            suppeliers_data = json.load(file)
            for supp in suppeliers_data:
                if not Suppelier.query.filter_by(rut=supp["rut"]).first():
                    new_suppelier = Suppelier(
                        name=supp["name"],
                        website=supp["website"],
                        rut=supp["rut"]
                    )
                    db.session.add(new_suppelier)
                    db.session.flush()

                    for phone in supp.get("phones", []):
                        db.session.add(Phone(number=phone, supplier_id=new_suppelier.id))

                    if "address" in supp:
                        db.session.add(Address(
                            street=supp["address"]["street"],
                            street_number=supp["address"]["number"],
                            apartment=supp["address"].get("apartment"),
                            district=supp["address"]["district"],
                            supplier_id=new_suppelier.id
                        ))
            db.session.commit()
            print("Proveedores cargados")

        # Cargar productos
        with open("data_json/products.json", encoding="utf-8") as file:
            products_data = json.load(file)
            for prod in products_data:
                if not Product.query.filter_by(nombre=prod["nombre"], marca=prod["marca"]).first():
                    db.session.add(Product(
                        nombre=prod["nombre"],
                        marca=prod["marca"],
                        stock=prod["stock"],
                        precio_actual=prod["precio_actual"],
                        category_id=prod["category_id"],
                        suppelier_id=prod["suppelier_id"]
                    ))
            db.session.commit()
            print("Productos cargados")

        # Cargar ventas
        with open("data_json/sales.json", encoding="utf-8") as file:
            sales_data = json.load(file)
            for sale in sales_data:
                if not Sale.query.filter_by(id=sale["id"]).first():
                    new_sale = Sale(
                        date=sale["date"],
                        client_id=sale["client_id"],
                        discount=sale["discount"],
                        total=sale["total"]
                    )
                    db.session.add(new_sale)
                    db.session.flush()

                    for detail in sale["details"]:
                        db.session.add(SaleDetail(
                            sale_id=new_sale.id,
                            product_id=detail["product_id"],
                            quantity=detail["quantity"],
                            unit_price=detail["unit_price"],
                            subtotal=detail["subtotal"]
                        ))
            db.session.commit()
            print("Ventas y detalles cargados")

    except Exception as e:
        db.session.rollback()
        print(f"Error al cargar datos: {e}")