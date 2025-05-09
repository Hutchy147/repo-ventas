from flask import Blueprint,request,jsonify
from database import db
from model.suppelier import Suppelier
from model.phone import Phone
from model.address import Address
suppelier=Blueprint("suppelier",__name__)

@suppelier.route("/get_suppelier",methods=["GET"])#Recibo los datos de los proveedores

def get_suppelier():
    suppeliers=Suppelier.query.all()#Obtengo los datos de los proveedores en la base de datos
    
    return jsonify([suppelier.to_dict() for suppelier in suppeliers])

@suppelier.route("/post_suppelier",methods=["POST"])#Agregar a nuevos proveedores

def post_suppelier():
    data=request.get_json()
    
    attributes=["name","website","rut"]
    missing=[key for key in attributes if key not in data]
    
    if not data or missing:
        return jsonify({"Error":"Faltan datos","Faltantes":missing})
    if Suppelier.query.filter_by(rut=data["rut"]).first():#verifico si el rut del proveedor ya existe
        return jsonify({"Error": "Rut ya registrado"}),400
    if Suppelier.query.filter_by(website=data["website"]).first():#verifico si la pagina del proveedor ya existe
        return jsonify({"Error": "website ya registrado"}),400

    
    try:

        new_suppelier=Suppelier(
            name=data["name"],
            phone=data["phone"],
            website=data["website"],
            rut=data["rut"])
        

        db.session.add(new_suppelier)
        db.session.flush()
        for number in data.get("phones", []):
            db.session.add(Phone(number=number, client_id=new_suppelier.id))

        address_data = data.get("address")
        if address_data:
            db.session.add(Address(
                street=address_data["street"],
                number=address_data["number"],
                apartment=address_data.get("apartment"),
                district=address_data["district"],
                suppelier_id=new_suppelier.id
            ))
        
        db.session.commit()
        return jsonify(new_suppelier.to_dict()),201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),500

@suppelier.route("/put_suppelier/<int:id>",methods=["PUT"])#actaulizar al proveedor completamente

def put_suppelier(id):
    suppelier=Suppelier.query.get(id)
    if not suppelier:
        return jsonify({"Menssje":"Proveedor no encontrado"}),404
    
    try:
        data=request.get_json()
        suppelier.name = data.get("name",suppelier.name)
        suppelier.website = data.get("website",suppelier.website)
        suppelier.rut = data.get("rut",suppelier.rut)
        if "address" in data:
            address_data=data["address"]
            if suppelier.address:
                suppelier.address.street = address_data.get("street",suppelier.address.street)
                suppelier.address.number = address_data.get("number",suppelier.address.number)
                suppelier.address.apartment = address_data.get("apartment",suppelier.address.apartment)
                suppelier.address.district = address_data.get("district",suppelier.address.district)
            else:
                suppelier.address = Address(
                    street=address_data["street"],
                    number=address_data["number"],
                    apartment=address_data["apartment"],
                    district=address_data["district"],
                    suppelier=suppelier
                )
        if "phones" in data:
            suppelier.phones.clear()
            for phone_number in data["phones"]:
                suppelier.phones.append(Phone(number=phone_number))

        db.session.commit()
        return jsonify({"Mensaje":"Proveedor actualizado"}),200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}),500
    
@suppelier.route("/patch_suppelier/<int:id>",methods =["PATCH"])#actualiza al proveedor por parte
def patch_suppelier(id):
    suppelier=Suppelier.query.get(id)
    data=request.get_json()

    if not suppelier:
        return jsonify({"Mensaje":"Proveedor no encontrado"}),404
    try:
        if "name" in data and data["name"]:
            suppelier.name = data["name"]

        if "website" in data and data["website"]:
            suppelier.website = data["website"]
        
        if "rut" in data and data ["rut"]:
            suppelier.rut = data["rut"]
        if "address" in data:
            address_data=data["address"]
            if suppelier.address:
                suppelier.address.street = address_data.get("street",suppelier.address.street)
                suppelier.address.number = address_data.get("number",suppelier.address.number)
                suppelier.address.apartment = address_data.get("apartment",suppelier.address.apartment)
                suppelier.address.district = address_data.get("district",suppelier.address.district)
            else:
                suppelier.address = Address(
                    street=address_data["street"],
                    number=address_data["number"],
                    apartment=address_data["apartment"],
                    district=address_data["district"],
                    suppelier=suppelier)
        if "phones" in data:
            suppelier.phones.clear()
            for phone_number in data["phones"]:
                suppelier.phones.append(Phone(number=phone_number))

        db.session.commit()
        return jsonify({"Mensaje":"Proveedor actualizado"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}),500

@suppelier.route("/delete_suppelier/<int:id>",methods=["DELETE"])

def delete_suppelier(id):
    suppelier=Suppelier.query.get(id)
    if not suppelier:
        return jsonify({"Mensaje":"No se encuentra proveedor"}),404
    
    try:
        db.session.delete(suppelier)
        db.session.commit()
        return jsonify({"Mensaje":"Proveedor eliminado"}),200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),500



