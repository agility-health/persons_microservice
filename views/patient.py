from hashlib import new
from flask import Blueprint, jsonify, request, Response
from config import db
from models.patient import Patient, Address
from schemas import patient_schema, patients_schema,\
                    address_schema
from services.auth import token_required, get_user_from_request
from services.services import get_object_by_id, is_equal_user_from_request_with_user_db

patient_view = Blueprint("patient", __name__)


@patient_view.route("/patients", methods=["Get"])
def get_patients():
    return jsonify(patients_schema.dump(Patient.query.all()))


@token_required
@patient_view.route("/patients", methods=["Post"])
def create_patient():
    user = get_user_from_request(request)
    patient_data = patient_schema.load(request.json)
    new_patient = Patient(**patient_data)
    new_patient.user = user
    db.session.add(new_patient)
    db.session.commit()
    return Response(patient_schema.dumps(new_patient), status=201, mimetype='application/json')



@patient_view.route("/patient/<patient_id>", methods=["Get"])
def get_patient_by_id(patient_id):
    patient = get_object_by_id(Model=Patient, id=patient_id)
    return Response(patient_schema.dumps(patient), status=200, mimetype='application/json')

@token_required
@patient_view.route("/patient/<patient_id>", methods=["Put"])
def update_patient(patient_id):
    user =  get_user_from_request(request)
    patient = get_object_by_id(Model=Patient, id=patient_id)
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=patient.user):
        return Response(status=403)    
    patient_data = patient_schema.load(request.json)
    db.session.query(Patient).filter(Patient.id == patient_id).update(patient_data)
    db.session.commit()
    
    return Response(status=200)

@token_required
@patient_view.route("/patient/<patient_id>", methods=["Delete"])
def delete_patient(patient_id):
    user =  get_user_from_request(request)
    patient = get_object_by_id(Model=Patient, id=patient_id)
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=patient.user):
        return Response(status=403)
    
    db.session.delete(Patient.query.filter_by(id=patient_id).first())
    db.session.commit()

    return Response(status=204)


@patient_view.route("/patient/<patient_id>/address", methods=["Get"])
def get_address(patient_id):
    patient = get_object_by_id(Model=Patient, id=patient_id)
    address = patient.address
    return Response(address_schema.dumps(address), status=200, mimetype='application/json')

@token_required
@patient_view.route("/patient/<patient_id>/address", methods=["Post"])
def create_address(patient_id):
    user =  get_user_from_request(request)
    patient = get_object_by_id(Model=Patient, id=patient_id)
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=patient.user):
        return Response(status=403)
    
    if patient.address:
        return Response("patient already have address", status=400)
    
    address_data = address_schema.load(request.json)
    new_address = Address(**address_data)
    patient.address =  new_address
    db.session.add(new_address)
    db.session.commit()

    return Response(address_schema.dumps(new_address), status=201, mimetype='application/json')

@token_required
@patient_view.route("/patient/<patient_id>/address", methods=["Put"])
def update_address(patient_id):
    user =  get_user_from_request(request)
    patient = get_object_by_id(Model=Patient, id=patient_id)
    
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=patient.user):
        return Response(status=403)
    
    if not patient.address:
        return Response("patient dont have address", status=400)

    address_data = address_schema.load(request.json)
    Address.query.filter_by(id=patient.address.id).update(address_data)
    
    db.session.commit()

    return Response(status=200)

@token_required
@patient_view.route("/patient/<patient_id>/address", methods=["Delete"])
def delete_address(patient_id):
    user =  get_user_from_request(request)
    patient = get_object_by_id(Model=Patient, id=patient_id)

    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=patient.user):
        return Response(status=403)
    
    if not patient.address:
        return Response("patient dont have address", status=400)

    db.session.delete(Address.query.filter_by(id=patient.address.id).first())
    db.session.commit()

    return Response(status=204)
