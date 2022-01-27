from dotenv import load_dotenv
from flask import request, Blueprint

from models.user import User
from config import db
from services.auth import create_token, create_access_token

my_view = Blueprint("views", __name__)


load_dotenv()


@my_view.route("/registration", methods=["Post"])
def registration_user():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]
    if User.query.filter_by(email=email).first() is not None:
         return {'message': f'User with {email} email already exists'}
    new_user = User(name=name, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return create_token(email)


@my_view.route("/login", methods=["Post"])
def login():
    email = request.json["email"]
    password = request.json["password"]
    user =User.query.filter_by(email=email).first()
    if user is None:
         return {'message': f"User with {email} email don't exists"}
    if user.check_password(password):
        return create_token(user.email)


@my_view.route("/refresh_token", methods=["Post"])
def refresh():
    token = request.json['refresh_token']
    return create_access_token(token)
