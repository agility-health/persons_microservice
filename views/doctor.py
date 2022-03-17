from schemas import educations_schema, education_schema, doctors_schema, doctor_schema
from flask import Blueprint, jsonify, request
from models.doctor import Doctor, Education
from config import db
from services.auth import token_required, get_user_from_token

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

@token_required
@doctor_view.route("/doctor", methods=["Post"])
def create_doctor():
    user = get_user_from_token(request)
    new_doctor = Doctor(
        first_name = request.json["first_name"],
        surname = request.json["surname"],
        birthday = request.json["birthday"],
        education = get_education_from_request(request.json["education"])
    )
    user.doctor = new_doctor
    db.session.add(new_doctor)
    db.session.add(user)
    db.session.commit()

    return doctor_schema.dump(new_doctor)


@doctor_view.route("/education", methods=["Post"])
def create_education():
    doctors = []
    doctors.append(Doctor.query.filter_by(id=1).first())
    new_education = Education(
        university_name = request.json["university_name"],
        specialization = request.json["specialization"],
        education_degree = request.json["education_degree"],
        date_of_graduation = request.json["date_of_graduation"],
    )

    db.session.add(new_education)
    db.session.commit()

    return education_schema.dump(new_education)

@doctor_view.route("/education", methods=["Get"])
def get_education():
    return jsonify(educations_schema.dump(Education.query.all()))

@doctor_view.route("/doctors", methods=["Get"])
def get_doctors():
    return jsonify(doctors_schema.dump(Doctor.query.all()))
