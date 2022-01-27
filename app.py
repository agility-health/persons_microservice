import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from redis import Redis

from producer import Producer


load_dotenv()

REDIS_HOST = '127.0.0.1'
prod = Producer("mystream", host=REDIS_HOST, port=6379, db=0)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
CORS(app)

r = Redis(host=REDIS_HOST, port=6379, db=0)
from views import my_view
app.register_blueprint(my_view)
