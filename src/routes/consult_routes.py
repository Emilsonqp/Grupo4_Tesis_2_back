from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..commands.create_consult import CreateConsult

consult_routes = Blueprint('consult_routes', __name__)

@consult_routes.route('/consults', methods = ['POST'])
@jwt_required()
def create():
    current_email = get_jwt_identity()
    consult = CreateConsult(current_email, request.get_json()).execute()
    return jsonify(consult), 201