from .base_command import BaseCommannd
from ..errors.errors import InvalidUserCredentials, InvalidParams
from ..models.user import User, UserJsonSchema
from ..session import Session
from flask_jwt_extended import create_access_token
from flask import has_app_context

class LoginUser(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        session = Session()
        try:
            if 'email' not in self.data or 'password' not in self.data:
                raise InvalidParams()

            user = session.query(User).filter_by(email=self.data['email']).first()

            if not user:
                raise InvalidUserCredentials()

            if not user.match_password(self.data['password']):
                raise InvalidUserCredentials()

            access_token = create_access_token(identity=self.data['email'])
            user = UserJsonSchema().dump(user)
            if has_app_context():
                access_token = create_access_token(identity=self.data['email'])
                user['token'] = access_token

            session.close()

            return user
        except Exception as error:
            session.close()
            raise error
