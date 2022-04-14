from datetime import datetime
from telnetlib import STATUS
from models.user import User
from schemas import educations_schema, education_schema, doctors_schema, doctor_schema
from flask import Blueprint, jsonify, request, Response
from models.doctor import Doctor, Education
from config import db
from services.auth import token_required, get_user_from_request
from services.doctor import is_have_education        
from services.services import get_object_by_id


doctor_view = Blueprint("doctor", __name__)

@doctor_view.route("/user/<id>/doctor", methods=["Get"])
def get_doctor(id):
    user = get_object_by_id(User, id)
    return doctor_schema.dump(user.doctor)

@token_required
@doctor_view.route("/user/<id>/doctor", methods=["Post"])
def create_doctor(id):
    user = get_user_from_request(request)
    if not user.id == int(id):
        return Response(status=403)
    if user.doctor:
        return Response("user already have doctor", status=400)
    doctor_data = doctor_schema.load(request.json)
    new_doctor = Doctor(**doctor_data)
    user.doctor = new_doctor
    db.session.add(new_doctor)
    db.session.commit()
    return Response(doctor_schema.dumps(new_doctor), status=201, mimetype='application/json')

@token_required
@doctor_view.route("/user/<id>/doctor", methods=["Put"])
def put_doctor(id):
    user = get_user_from_request(request)
    if not user.id == int(id):
        return Response(status=403)
    doctor_data = doctor_schema.load(request.json)
    Doctor.query.filter_by(id=user.doctor.id).update(doctor_data)
    db.session.commit()
    return Response(status=200)

@token_required
@doctor_view.route("/user/<id>/doctor", methods=["Delete"])
def delete_doctor(id):
    user = get_user_from_request(request)
    if not user.id == int(id):
        return Response(status=403)
    db.session.delete(user.doctor)
    db.session.commit()
    return Response(status=204)


@doctor_view.route("/user/<id>/doctor/education", methods=["Get"])
def get_all_education(id):
    user = get_object_by_id(User, id)
    if is_have_education(user):
        return is_have_education(user)
    return Response(educations_schema.dumps(user.doctor.education), status=200, mimetype='application/json')

@doctor_view.route("/user/<user_id>/doctor/education/<education_id>", methods=["Get"])
def get_education(user_id, education_id):
    user = get_object_by_id(User, user_id)
    if is_have_education(user):
        return is_have_education(user)
    education = next((education for education in user.doctor.education if education.id == int(education_id)), None)
    
    return Response(education_schema.dumps(education), status=200, mimetype='application/json')


@token_required
@doctor_view.route("/user/<user_id>/doctor/education", methods=["Post"])
def create_education(user_id):
    user = get_object_by_id(User, user_id)
    if not user.id == int(user_id):
        return Response(status=403)
    
    education_data = education_schema.load(request.json)
    new_education = Education(**education_data)
    user.doctor.education.append(new_education)
    db.session.add(new_education)
    db.session.commit()

    return Response(education_schema.dumps(new_education), status=201, mimetype='application/json')


@token_required
@doctor_view.route("/user/<user_id>/doctor/education/<education_id>", methods=["Put"])
def update_education(user_id, education_id):
    user = get_object_by_id(User, user_id)
    if not user.id == int(user_id):
        return Response(status=403)
    if is_have_education(user):
        return is_have_education(user)
    education = next((education for education in user.doctor.education if education.id == int(education_id)), None)
    
    if not education:
        return Response("education with this id user dont have", status=400)
    
    education_data = education_schema.load(request.json)
    db.session.query(Education).filter_by(id=education_id).update(education_data)
    db.session.commit()
    return Response(
        education_schema.dumps(Education.query.filter_by(id=education_id).one()),
        status=200,
        mimetype='application/json'
        )

@token_required
@doctor_view.route("/user/<user_id>/doctor/education/<education_id>", methods=["Delete"])
def delete_education(user_id, education_id):
    user = get_object_by_id(User, user_id)
    if not user.id == int(user_id):
        return Response(status=403)
    if is_have_education(user):
        return is_have_education(user)
    
    education = next((education for education in user.doctor.education if education.id == int(education_id)), None)
    if not education:
        return Response("education with this id user dont have", status=400)
    
    db.session.delete(education)
    db.session.commit()
    
    return Response(status=204)
