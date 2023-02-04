from flask import jsonify, Blueprint, request

from ..commands.login_user import LoginUser
from ..commands.signup_user import SignupUser

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods = ['POST'])
def create():
    user = SignupUser(request.get_json()).execute()
    return jsonify(user), 201


@user_routes.route('/users/login', methods = ['POST'])
def login():
    user = LoginUser(request.get_json()).execute()
    return jsonify(user), 201