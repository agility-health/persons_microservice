from datetime import datetime
from schemas import educations_schema, education_schema, doctors_schema, doctor_schema
from flask import Blueprint, jsonify, request, Response
from models.doctor import Doctor, Education
from config import db
from services.auth import token_required, get_user_from_request
from services.doctor import get_doctor_by_id,\
     is_equal_user_from_request_with_user_db        
from services.services import get_object_by_id


doctor_view = Blueprint("doctor", __name__)


@doctor_view.route("/doctors", methods=["Get"])
def get_doctors():
    return jsonify(doctors_schema.dump(Doctor.query.all()))

@token_required
@doctor_view.route("/doctor", methods=["Post"])
def create_doctor():
    user = get_user_from_request(request)
    doctor_data = doctor_schema.load(request.json)
    new_doctor = Doctor(**doctor_data)
    if user.doctor:
        return Response("{'message':'user already have a doctor'}", status=400, mimetype='application/json')     
    else:
        user.doctor = new_doctor
    db.session.add(new_doctor)
    db.session.commit()

    return Response(doctor_schema.dumps(new_doctor), status=201, mimetype='application/json')


@doctor_view.route("/doctor/<id>", methods=["Get"])
def get_doctor(id):
    doctor = get_doctor_by_id(id)
    return doctor_schema.dump(doctor)

@token_required
@doctor_view.route("/doctor/<id>", methods=["Put"])
def put_doctor(id):
    user = get_user_from_request(request)
    doctor = get_doctor_by_id(id)
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=doctor.user):
        return Response(status=403)
    doctor_data = doctor_schema.load(request.json)
    Doctor.query.filter_by(id=doctor.id).update(doctor_data)
    db.session.commit()
    return Response(status=200)

@token_required
@doctor_view.route("/doctor/<id>", methods=["Delete"])
def delete_doctor(id):
    user = get_user_from_request(request)
    doctor = get_doctor_by_id(id)
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=doctor.user):
        return Response(status=403)
    db.session.delete(doctor)
    db.session.commit()
    return Response(status=204)

@token_required
@doctor_view.route("/doctor/<doctor_id>/education", methods=["Post"])
def create_education(doctor_id):
    user = get_user_from_request(request)
    doctor = get_doctor_by_id(doctor_id)
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=doctor.user):
        return Response(status=403)
    
    education_data = education_schema.load(request.json)
    new_education = Education(**education_data)
    doctor.education.append(new_education)
    db.session.add(new_education)
    db.session.commit()

    return Response(education_schema.dumps(new_education), status=201, mimetype='application/json')

@doctor_view.route("/doctor/<doctor_id>/education", methods=["Get"])
def get_education(doctor_id):
    doctor = get_doctor_by_id(doctor_id)
    return Response(educations_schema.dumps(doctor.education), status=200, mimetype='application/json')

@doctor_view.route("/doctor/<doctor_id>/education/<education_id>", methods=["Get"])
def get_education_by_id(doctor_id, education_id):
    education = get_object_by_id(Model=Education, id=education_id)
    return Response(education_schema.dumps(education), status=200, mimetype='application/json')

@token_required
@doctor_view.route("/doctor/<doctor_id>/education/<education_id>", methods=["Put"])
def update_education_by_id(doctor_id, education_id):
    user = get_user_from_request(request)
    doctor = get_doctor_by_id(doctor_id)
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=doctor.user):
        return Response(status=403)
    education_data = education_schema.load(request.json)
    Education.query.filter_by(id=education_id).update(education_data)
    db.session.commit()
    return Response(status=200)

@token_required
@doctor_view.route("/doctor/<doctor_id>/education/<education_id>", methods=["Delete"])
def delete_education_by_id(doctor_id, education_id):
    user = get_user_from_request(request)
    doctor = get_doctor_by_id(doctor_id)
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=doctor.user):
        return Response(status=403)
    education = get_object_by_id(Model=Education, id=education_id)
    db.session.delete(education)
    db.session.commit()
    return Response(status=204)
