from dataclasses import field
import email
from models.doctor import Doctor
from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    name = fields.String()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class EducationSchema(Schema):
    id = fields.Integer()
    university_name = fields.String()
    specialization = fields.String()
    education_degree = fields.String()
    date_of_graduation = fields.Date()

education_schema = EducationSchema()
educations_schema = EducationSchema(many=True)


class DoctorSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    surname = fields.String()
    birthday = fields.Date()
    education = fields.List(fields.Nested(EducationSchema))

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)


class AddressSchema(Schema):
    id = fields.Integer()
    country = fields.String()
    city = fields.String()
    street = fields.String()
    house_number = fields.String()
    number_flat = fields.String()

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)


class PhoneSchema(Schema):
    id = fields.Integer()
    country_code = fields.Integer()
    area_code = fields.Integer()
    number = fields.Integer()

phone_schema = PhoneSchema()
phones_schema = PhoneSchema(many=True)


class PatientSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    surname = fields.String()
    birthday = fields.Date()
    address = fields.Nested(AddressSchema)
    phone = fields.Nested(PhoneSchema)

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)
