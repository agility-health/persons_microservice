from flask import Blueprint, jsonify, request, Response
from config import db
from models.user import User
from models.patient import Patient, Address
from schemas import patient_schema, patients_schema, address_schema, addresses_schema
from services.auth import token_required, get_user_from_request
from services.services import get_object_by_id

patient_view = Blueprint("patient", __name__)


@patient_view.route("/patients", methods=["Get"])
def get_patients():
    return jsonify(patients_schema.dump(Patient.query.all()))


@patient_view.route("/user/<id>/patient", methods=["Get"])
def get_patient(id):
    user = get_object_by_id(Model=User, id=id)
    return Response(
        patient_schema.dumps(user.patient), status=200, mimetype="application/json"
    )


@token_required
@patient_view.route("/user/<id>/patient", methods=["Post"])
def create_patient(id):
    user = get_user_from_request(request)
    if not user.id == int(id):
        return Response(status=403)
    if user.patient:
        return Response("user already have patient", status=400)
    patient_data = patient_schema.load(request.json)
    new_patient = Patient(**patient_data)
    user.patient = new_patient
    db.session.add(new_patient)
    db.session.commit()
    return Response(
        patient_schema.dumps(new_patient), status=201, mimetype="application/json"
    )


@token_required
@patient_view.route("/user/<id>/patient", methods=["Put"])
def update_patient(id):
    user = get_user_from_request(request)
    if not user.id == int(id):
        return Response(status=403)
    if not user.patient:
        return Response("user dont have patient", status=400)
    patient_data = patient_schema.load(request.json)
    Patient.query.filter_by(id=user.patient.id).update(patient_data)
    db.session.commit()
    return Response(
        patient_schema.dumps(Patient.query.filter_by(id=user.patient.id).one()),
        status=201,
        mimetype="application/json",
    )


@token_required
@patient_view.route("/user/<id>/patient", methods=["Delete"])
def delete_patient(id):
    user = get_user_from_request(request)
    if not user.id == int(id):
        return Response(status=403)
    if not user.patient:
        return Response("user dont have patient", status=400)
    db.session.delete(Patient.query.filter_by(id=user.patient.id).one())
    db.session.commit()
    return Response(status=204)


@patient_view.route("/user/<id>/patient/address", methods=["Get"])
def get_address(id):
    user = get_object_by_id(Model=User, id=id)
    if not user.patient:
        return Response("user dont have patient", status=400)
    if not user.patient.address:
        return Response({}, status=200, mimetype="application/json")
    return Response(
        address_schema.dumps(
            Address.query.filter_by(id=user.patient.address_id).one_or_none()
        ),
        status=200,
        mimetype="application/json",
    )


@token_required
@patient_view.route("/user/<id>/patient/address", methods=["Post"])
def create_address(id):
    user = get_user_from_request(request)
    if not user.id == int(id):
        return Response(status=403)
    if not user.patient:
        return Response("user dont have patient", status=400)
    if user.patient.address:
        return Response("patient already have address", status=400)

    address_data = address_schema.load(request.json)
    new_address = Address(**address_data)
    user.patient.address = new_address
    db.session.add(new_address)
    db.session.commit()
    return Response(
        address_schema.dumps(new_address), status=201, mimetype="application/json"
    )


@token_required
@patient_view.route("/user/<id>/patient/address", methods=["Put"])
def update_address(id):
    user = get_user_from_request(request)
    if not user.id == int(id):
        return Response(status=403)
    if not user.patient:
        return Response("user dont have patient", status=400)
    if not user.patient.address:
        return Response("patient dont have address", status=400)

    address_data = address_schema.load(request.json)
    Address.query.filter_by(id=user.patient.address.id).update(address_data)
    db.session.commit()
    return Response(
        address_schema.dumps(Address.query.filter_by(id=user.patient.address.id).one()),
        status=200,
        mimetype="application/json",
    )


@token_required
@patient_view.route("/user/<id>/patient/address", methods=["Delete"])
def delete_address(id):
    user = get_user_from_request(request)
    if not user.id == int(id):
        return Response(status=403)
    if not user.patient:
        return Response("user dont have patient", status=400)
    if not user.patient.address:
        return Response("patient dont have address", status=400)

    db.session.delete(Address.query.filter_by(id=user.patient.address.id).one())
    db.session.commit()
    return Response(status=204)
