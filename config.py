from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
