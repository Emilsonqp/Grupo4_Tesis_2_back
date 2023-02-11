import os

from flask import Flask, jsonify
from flask_wtf.csrf import CSRFProtect
from .session import engine
from .models.model import Base
from .routes.base_routes import base_routes
from .routes.user_routes import user_routes
from .routes.specialist_routes import specialist_routes
from .routes.consult_routes import consult_routes
from .errors.errors import ApiError
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.register_blueprint(base_routes)
app.register_blueprint(user_routes)
app.register_blueprint(specialist_routes)
app.register_blueprint(consult_routes)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY'] if 'JWT_SECRET_KEY' in os.environ else 'ROCK&ROLL_TRAIN_ACDC'

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

Base.metadata.create_all(engine)
jwt = JWTManager(app)


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description 
    }
    return jsonify(response), err.code

jwt = JWTManager(app)