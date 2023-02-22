from .base_command import BaseCommannd
from ..models.consult import Consult, ConsultJsonSchema
from ..session import Session
from ..errors.errors import InvalidParams, SpecialistIsNotRegister, SpecialistWrongPassword
from ..commands.get_specialist import GetSpecialist

class UserConsults(BaseCommannd):
    def __init__(self, user_id):
        self.user_id = user_id

    def execute(self):
      session = Session()
      consults = session.query(Consult).filter_by(user_id=self.user_id).order_by(Consult.created_at.desc())
      consults = ConsultJsonSchema(many=True).dump(consults)
      session.close()

      for consult in consults:
        if consult['specialist_id'] != None:
            specialist = GetSpecialist(consult['specialist_id']).execute()
            consult['specialist'] = specialist
        else:
            consult['specialist'] = None

      return consults