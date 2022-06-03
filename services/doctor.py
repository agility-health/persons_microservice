from flask import Response
from models.doctor import Doctor


def is_have_education(user):
    if not bool(user.doctor):
        return Response("user dont have doctor", status=400)
    if not bool(user.doctor.education):
        return Response("doctor dont have education", status=400)
