import datetime
import os
from dotenv import load_dotenv
from flask import request, jsonify
import jwt
from functools import wraps

from app import app
from models.user import User

load_dotenv()


def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]
        if not token:
            return jsonify({"message": "a valid token is missing"})

        try:
            if verify_access_token(token):
                return f(*args, **kwargs)
        except jwt.exceptions.InvalidSignatureError:
            jsonify({"message": "token is invalid"})
        except jwt.exceptions.ExpiredSignatureError:
            jsonify({"message": "token is Expired"})
        return jsonify({"message": "token is invalid"})

    return decorator


def create_access_token(refresh_token):
    is_valid_token, payload = verify_refresh_token(refresh_token)
    if is_valid_token:
        access_token = jwt.encode(
            payload, app.config["SECRET_KEY"], os.getenv("ALGORITHM")
        )
        return {"access_token": access_token}
    return jsonify({"message": "refresh token is not valid"})


def create_token(email, id):
    payload = {
        "id": id,
        "email": email,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=float(os.getenv("TOKEN_LIFETIME"))),
        "grant_type": "access",
    }
    access_token = jwt.encode(payload, app.config["SECRET_KEY"], os.getenv("ALGORITHM"))
    payload["grant_type"] = "refresh"
    refresh_token = jwt.encode(payload, app.config["SECRET_KEY"], os.getenv("ALGORITHM"))
    return {"access_token": access_token, "refresh_token": refresh_token}


def verify_refresh_token(token):
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], os.getenv("ALGORITHM"))
        if payload and payload.get("grant_type") == "refresh":
            payload["grant_type"] = "access"
            return True, payload
        return False, None
    except jwt.exceptions.InvalidSignatureError:
        return jsonify({"message": "token is not valid"})


def verify_access_token(token):
    payload = jwt.decode(token, app.config["SECRET_KEY"], os.getenv("ALGORITHM"))
    if payload and not payload.get("grant_type") == "refresh":
        return True, payload
    return False


def get_user_from_request(request):
    token = request.headers["x-access-tokens"]
    payload = jwt.decode(token, app.config["SECRET_KEY"], os.getenv("ALGORITHM"))
    return User.query.filter_by(id=payload.get("id")).first()


def get_user_from_token(token):
    payload = jwt.decode(token, app.config["SECRET_KEY"], os.getenv("ALGORITHM"))
    return User.query.filter_by(id=payload.get("id")).first()
