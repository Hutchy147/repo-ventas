from flask import Blueprint,request,jsonify
from database import db
from model.suppelier import Suppelier

suppelier=Blueprint("suppelier",__name__)

@suppelier.route("/get_suppelier",methods=["GET"])

def get_suppelier():
    suppeliers=Suppelier.query.all()#Obtengo los datos de los proveedores en la base de datos
    
    return jsonify([suplier.serialize() for suplier in suppeliers])

@suppelier.route("/post_suppelier",methods=["POST"])

def post_suppelier():
    data=request.get_json()
    
    attributes=["name","phone","website","rut"]
    missing=[key for key in attributes if key not in data]
    
    if not data or missing:
        return jsonify({"Error":"Faltan datos","Faltantes":missing})
    if Suppelier.query.filter_by(rut=data["rut"]).first():#verifico si el rut del proveedor ya existe
        return jsonify({"Error": "Rut ya registrado"}),400
    
    if Suppelier.query.filter_by(phone=data["phone"]).first():#verifico si el telefono del proveedor ya existe
        return jsonify({"Error": "phone ya registrado"}),400
    
    if Suppelier.query.filter_by(website=data["website"]).first():#verifico si la pagina del proveedor ya existe
        return jsonify({"Error": "website ya registrado"}),400

    
    try:

        new_suppelier=Suppelier(
            name=data["name"],
            phone=data["phone"],
            website=data["website"],
            rut=data["rut"])
        
        db.session.add(new_suppelier)
        db.session.commit()
        return jsonify(new_suppelier.serialize()),201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),500
    
@suppelier.route("/delete_suppelier/<int:id>",methods=["DELETE"])

def delete_suppelier(id):
    suppelier=Suppelier.query.get(id)
    if not suppelier:
        return jsonify({"Mensaje":"No se encuentra proveedor"}),404
    
    try:
        db.session.delete(suppelier)
        db.session.commit()
        return jsonify({"Mensaje":"Proveedor eliminado"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),500



