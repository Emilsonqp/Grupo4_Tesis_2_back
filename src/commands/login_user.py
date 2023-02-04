from .base_command import BaseCommannd
from ..errors.errors import InvalidUserCredentials, InvalidParams
from ..models.user import User
from ..session import Session
from flask_jwt_extended import create_access_token


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

            session.close()

            return {'token': access_token}
        except Exception as error:
            session.close()
            raise error
