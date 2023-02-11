from .base_command import BaseCommannd
from ..session import Session
from ..models.user import User, UserJsonSchema
from ..errors.errors import UserDoesNotExit

class UserDetail(BaseCommannd):
    def __init__(self, user_id):
        self.user_id = user_id

    def execute(self):
        session = Session()
        user = session.query(User).filter_by(id=self.user_id).first()
        if not user:
            session.close()
            raise UserDoesNotExit()
        
        user = UserJsonSchema().dump(user)
        session.close()
        return user