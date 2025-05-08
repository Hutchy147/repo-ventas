from flask import Blueprint,request,jsonify
from Database import db
from model.suplier import Suplier

suplier=Blueprint("suplier",__name__)

@suplier.route("/api/get_suplier",methods=["GET"])

def get_suplier():
    supliers=Suplier.query.all()#Obtengo los datos de los proveedores en la base de datos
    
    return jsonify([suplier.serialize() for suplier in supliers])

@suplier.route("/api/post_suplier",methods=["POST"])

def post_suplier():
    data=request.get_json()
    
    if not data or not all(key in data for key in ["name","adress","website","rut"]):
        return jsonify({"Error":"Datos no encontrados"}),400
    
    if Suplier.query.filter_by(rut=data["rut"]).first():#verifico si el rut del proveedor ya existe
        return jsonify({"Error": "Rut ya registrado"}),400
    
    try:

        new_suplier=Suplier(data["name"],data["adress"],data["website"],data["rut"])
        db.session.add(new_suplier)
        db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),500
    
@suplier.route("/api/delete_suplier",methods=["DELETE"])

def delete_suplier(id):
    suplier=Suplier.query.get(id)
    if not suplier:
        return jsonify({"Mensaje","No se encuentra proveedor"}),404
    
    try:
        db.session.delete(suplier)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),500



