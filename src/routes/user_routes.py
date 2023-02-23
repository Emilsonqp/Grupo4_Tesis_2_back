from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..commands.login_user import LoginUser
from ..commands.signup_user import SignupUser
from ..commands.update_user_city import UpdateUserCity
from ..commands.list_users import ListUsers
from ..commands.update_user_detail import UpdateUserDetail
from ..commands.user_detail import UserDetail
from ..commands.user_consults import UserConsults

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/users', methods=['POST'])
def create():
    user = SignupUser(request.get_json()).execute()
    return jsonify(user), 201


@user_routes.route('/users/login', methods=['POST'])
def login():
    user = LoginUser(request.get_json()).execute()
    return jsonify(user), 201


@user_routes.route('/users/update_city', methods=['PUT'])
@jwt_required()
def update_city():
    current_email = get_jwt_identity()
    user = UpdateUserCity(current_email, request.get_json()).execute()
    return jsonify(user)


@user_routes.route('/users/<id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = UpdateUserDetail(id, request.get_json()).execute()
    return jsonify(user)


@user_routes.route('/users', methods=['GET'])
@jwt_required()
def index():
    users = ListUsers().execute()
    return jsonify(users)


@user_routes.route('/users/<id>', methods=['GET'])
@jwt_required()
def show(id):
    user = UserDetail(id).execute()
    return jsonify(user)


@user_routes.route('/users/<id>/consults', methods=['GET'])
@jwt_required()
def consults(id):
    consults = UserConsults(id).execute()
    return jsonify({ "mssg": "Mi error", "msg": "Mi error" }), 500
