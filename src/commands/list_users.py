from .base_command import BaseCommannd
from ..session import Session
from ..models.user import User, UserJsonSchema

class ListUsers(BaseCommannd):
    def execute(self):
      session = Session()
      users = session.query(User).all()
      users = UserJsonSchema(many=True).dump(users)
      session.close()

      return users