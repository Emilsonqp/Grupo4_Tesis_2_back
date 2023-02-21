from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..commands.create_consult import CreateConsult
from ..commands.user_consults import UserConsults
from ..commands.get_user_by_email import GetUserByEmail
from ..commands.get_consult import GetConsult

consult_routes = Blueprint('consult_routes', __name__)

@consult_routes.route('/consults', methods = ['POST'])
@jwt_required()
def create():
    current_email = get_jwt_identity()
    consult = CreateConsult(current_email, request.get_json()).execute()
    return jsonify(consult), 201

@consult_routes.route('/consults', methods=['GET'])
@jwt_required()
def index():
    current_email = get_jwt_identity()
    user = GetUserByEmail(current_email).execute()
    consults = UserConsults(user['id']).execute()
    return jsonify(consults)

@consult_routes.route('/consults/<id>', methods=['GET'])
@jwt_required()
def show(id):
    consult = GetConsult(id).execute()
    return jsonify(consult)
