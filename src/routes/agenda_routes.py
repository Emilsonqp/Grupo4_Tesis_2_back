from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..commands.get_agenda import GetAgenda

agenda_specialist_routes = Blueprint('agenda_specialist_routes', __name__)

@agenda_specialist_routes.route('/agenda_specialist', methods = ['GET'])
@jwt_required()
def create():
    current_email = get_jwt_identity()
    consult = GetAgenda(current_email).execute()
    