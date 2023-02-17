from flask import jsonify, Blueprint, request
from ..commands.signup_specialist import SignupSpecialist
from ..commands.login_specialist import LoginSpecialist
from ..commands.list_specialists import ListSpecialistByEmail
from ..commands.update_specialist import UpdateSpecialist
from flask_jwt_extended import unset_jwt_cookies, jwt_required, get_jwt_identity

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

@specialist_routes.route('/specialist/profile/<current_email>', methods = ['GET'])
@jwt_required()
def getSpecialist(current_email):
    specialist = ListSpecialistByEmail(current_email).execute()
    return jsonify(specialist)

@specialist_routes.route('/specialist/update_profile', methods = ['PUT'])
@jwt_required()
def update_profile():
    current_email = get_jwt_identity()
    sp = UpdateSpecialist(current_email, request.get_json()).execute()
    return jsonify(sp)

@specialist_routes.route('/specialist/logout', methods = ['POST'])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response