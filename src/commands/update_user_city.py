from .base_command import BaseCommannd
from ..models.user import User, UserSchema, UserJsonSchema
from ..session import Session
from ..errors.errors import Unauthorized, InvalidParams
from datetime import datetime

class UpdateUserCity(BaseCommannd):
  def __init__(self, user_email, data):
    self.user_email = user_email
    self.data = data
  
  def execute(self):
    if 'city' not in self.data:
      raise InvalidParams()

    session = Session()
    user = session.query(User).filter_by(email=self.user_email).first()

    if user is None:
      session.close()
      raise Unauthorized()

    new_city = self.data['city']
    user.city = new_city
    session.commit()

    user = UserJsonSchema().dump(user)
    session.close()
    
    return user
    