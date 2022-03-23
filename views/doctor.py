from datetime import datetime
from schemas import educations_schema, education_schema, doctors_schema, doctor_schema
from flask import Blueprint, jsonify, request, Response
from models.doctor import Doctor, Education
from config import db
from services.auth import token_required, get_user_from_request
from services.doctor import get_doctor_by_id,\
     get_education_by_id_from_doctor,\
     is_equal_user_from_request_with_user_db        
from constants import DATE_FORMAT


doctor_view = Blueprint("doctor", __name__)


def get_education_from_request(education):
    education_from_db = []
    for ed in education:
        education_obj_db = Education.query.filter_by(
            university_name=ed["university_name"],
            specialization=ed["specialization"],
            education_degree=ed["education_degree"],
            date_of_graduation=ed["date_of_graduation"]).first()
        if education_obj_db:
            education_from_db.append(education_obj_db)
        else:
            new_education=Education(
                university_name=ed["university_name"],
                specialization=ed["specialization"],
                education_degree=ed["education_degree"],
                date_of_graduation=ed["date_of_graduation"]
            )
            db.session.add(new_education)
            education_from_db.append(new_education)

    return education_from_db

@doctor_view.route("/doctors", methods=["Get"])
def get_doctors():
    return jsonify(doctors_schema.dump(Doctor.query.all()))

@token_required
@doctor_view.route("/doctor", methods=["Post"])
def create_doctor():
    user = get_user_from_request(request)
    new_doctor = Doctor(
        first_name = request.json["first_name"],
        surname = request.json["surname"],
        birthday = request.json["birthday"],
        education = get_education_from_request(request.json["education"])
    )
    if user.doctor:
        return Response("{'message':'user already have a doctor'}", status=400, mimetype='application/json')     
    else:
        user.doctor = new_doctor
    db.session.add(new_doctor)
    db.session.commit()

    return Response(jsonify(doctor_schema.dump(new_doctor)), status=201, mimetype='application/json')


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
    doctor.first_name = request.json["first_name"]
    doctor.surname = request.json["surname"]
    doctor.birthday = datetime.strptime(request.json["birthday"], DATE_FORMAT)
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
    doctor.education = get_education_from_request(request.json)
    db.session.commit()

    return doctor_schema.dump(doctor)

@doctor_view.route("/doctor/<doctor_id>/education", methods=["Get"])
def get_education(doctor_id):
    doctor = get_doctor_by_id(doctor_id)
    return jsonify(educations_schema.dump(doctor.education))

@doctor_view.route("/doctor/<doctor_id>/education/<education_id>", methods=["Get"])
def get_education_by_id(doctor_id, education_id):
    doctor = get_doctor_by_id(doctor_id)
    education = get_education_by_id_from_doctor(doctor, education_id)
    return education_schema.dump(education)

@token_required
@doctor_view.route("/doctor/<doctor_id>/education/<education_id>", methods=["Put"])
def update_education_by_id(doctor_id, education_id):
    user = get_user_from_request(request)
    doctor = get_doctor_by_id(id)
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=doctor.user):
        return Response(status=403)
    education = get_education_by_id_from_doctor(doctor, education_id)
    education.university_name = request.json['university_name']
    education.specialization = request.json['specialization']
    education.education_degree = request.json['education_degree']
    education.date_of_graduation = datetime.strptime(request.json['date_of_graduation'], DATE_FORMAT)
    db.session.commit()
    return Response(status=200)

@token_required
@doctor_view.route("/doctor/<doctor_id>/education/<education_id>", methods=["Delete"])
def delete_education_by_id(doctor_id, education_id):
    user = get_user_from_request(request)
    doctor = get_doctor_by_id(id)
    if not is_equal_user_from_request_with_user_db(request_user=user, db_user=doctor.user):
        return Response(status=403)
    education = get_education_by_id_from_doctor(doctor, education_id)
    db.session.delete(education)
    db.session.commit()
    return Response(status=204)
