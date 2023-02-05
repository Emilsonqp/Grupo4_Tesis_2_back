from flask import Flask, jsonify
from flask_wtf.csrf import CSRFProtect
from .session import engine
from .models.model import Base
from .routes.base_routes import base_routes
from .routes.user_routes import user_routes
from .routes.specialist_routes import specialist_routes
from .errors.errors import ApiError
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.register_blueprint(base_routes)
app.register_blueprint(user_routes)
app.register_blueprint(specialist_routes)
app.config['JWT_SECRET_KEY'] = 'ROCK&ROLL_TRAIN_ACDC'

Base.metadata.create_all(engine)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description 
    }
    return jsonify(response), err.code

jwt = JWTManager(app)