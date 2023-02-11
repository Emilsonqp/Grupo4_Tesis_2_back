from .base_command import BaseCommannd
from ..models.consult import Consult, ConsultJsonSchema
from ..session import Session
from ..errors.errors import InvalidParams, SpecialistIsNotRegister, SpecialistWrongPassword

class UserConsults(BaseCommannd):
    def __init__(self, user_id):
        self.user_id = user_id

    def execute(self):
      session = Session()
      consults = session.query(Consult).filter_by(user_id=self.user_id).all()
      consults = ConsultJsonSchema(many=True).dump(consults)
      session.close()

      return consults