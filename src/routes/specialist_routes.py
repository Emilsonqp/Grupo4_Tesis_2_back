from flask import jsonify, Blueprint, request
from ..commands.signup_specialist import SignupSpecialist
from ..commands.login_specialist import LoginSpecialist
from flask_jwt_extended import unset_jwt_cookies, jwt_required

specialist_routes = Blueprint('specialist_routes', __name__)

@specialist_routes.route('/specialist', methods = ['POST'])
def create():
    specialist = SignupSpecialist(request.get_json()).execute()
    return jsonify(specialist), 201

@specialist_routes.route('/specialist/login', methods = ['POST'])
def login():
    specialist = LoginSpecialist(request.get_json()).execute()
    return jsonify(specialist), 201

@specialist_routes.route('/specialist/home', methods = ['POST'])
@jwt_required()
def home():
    response_body = {
        "mssg": "auth sucess!"
    }
    return response_body

@specialist_routes.route('/specialist/logout', methods = ['POST'])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response