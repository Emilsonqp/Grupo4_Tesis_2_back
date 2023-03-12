from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..commands.get_consults_by_filters import GetConsultsByFilters
from ..commands.create_consult import CreateConsult
from ..commands.user_consults import UserConsults
from ..commands.get_user_by_email import GetUserByEmail
from ..commands.get_consult import GetConsult, GetPendingConsults
from ..commands.update_consult_status import UpdateConsultStatus
from ..commands.list_consults_specialist import ConsultSpecialistUpdate
from ..commands.get_specialist_by_email import GetSpecialistByEmail
from ..commands.get_confirmed_consults import GetConfirmedConsults

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

@consult_routes.route('/pending_consults', methods=['GET'])
@jwt_required()
def showAllConsults():
    consult = GetPendingConsults().execute()
    return jsonify(consult)

@consult_routes.route('/confirmed_consults', methods=['GET'])
@jwt_required()
def showConfirmed():
    current_email = get_jwt_identity()
    specialist = GetSpecialistByEmail(current_email).execute()
    consults = GetConfirmedConsults(specialist['id']).execute()
    return jsonify(consults)

@consult_routes.route('/consults_by_filters', methods=['GET'])
@jwt_required()
def showFilter():
    current_email = get_jwt_identity()
    specialist = GetSpecialistByEmail(current_email).execute()
    consults = GetConsultsByFilters(specialist['id']).execute()
    return jsonify(consults)

@consult_routes.route('/consults/<id>', methods=['PUT'])
@jwt_required()
def update(id):
    consult = UpdateConsultStatus(id, request.get_json()).execute()
    return jsonify(consult)

@consult_routes.route('/consults_update/<id>', methods=['PUT'])
@jwt_required()
def update_consult(id):
    current_email = get_jwt_identity()
    id = request.get_json()["id"]
    description = request.get_json()["description"]
    diagnosis = request.get_json()["diagnosis"]
    consult = ConsultSpecialistUpdate(current_email, id, description, diagnosis).execute()
    return consult 

