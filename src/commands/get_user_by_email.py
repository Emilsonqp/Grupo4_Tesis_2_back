from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import InvalidParams, InvalidUserCredentials
from ..models.user import User, UserJsonSchema

class GetUserByEmail(BaseCommannd):
    def __init__(self, user_email):
        self.user_email = user_email

    def execute(self):
      session = Session()
      user = session.query(User).filter_by(email=self.user_email).first()
      if not user:
        session.close()
        raise InvalidUserCredentials()

      user = UserJsonSchema().dump(user)
      session.close()
      return user