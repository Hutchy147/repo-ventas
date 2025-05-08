from flask import Blueprint,request,jsonify
from database import db
from model.suppelier import Suppelier

suppelier=Blueprint("suppelier",__name__)

@suppelier.route("/api/get_suppelier",methods=["GET"])

def get_suppelier():
    suppeliers=Suppelier.query.all()#Obtengo los datos de los proveedores en la base de datos
    
    return jsonify([suplier.serialize() for suplier in suppeliers])

@suppelier.route("/api/post_suppelier",methods=["POST"])

def post_suppelier():
    data=request.get_json()
    
    if not data or not all(key in data for key in ["name","adress","website","rut"]):
        return jsonify({"Error":"Datos no encontrados"}),400
    
    if Suppelier.query.filter_by(rut=data["rut"]).first():#verifico si el rut del proveedor ya existe
        return jsonify({"Error": "Rut ya registrado"}),400
    
    try:

        new_suppelier=Suppelier(data["name"],data["adress"],data["website"],data["rut"])
        db.session.add(new_suppelier)
        db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),500
    
@suppelier.route("/api/delete_suppelier",methods=["DELETE"])

def delete_suppelier(id):
    suppelier=Suppelier.query.get(id)
    if not suppelier:
        return jsonify({"Mensaje","No se encuentra proveedor"}),404
    
    try:
        db.session.delete(suppelier)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),500



