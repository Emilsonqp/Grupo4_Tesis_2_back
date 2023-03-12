from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import InvalidParams, SpecialistIsNotRegister
from ..models.specialist import Specialist, SpecialistJsonSchema

class GetSpecialistByEmail(BaseCommannd):
    def __init__(self, specialist_email):
        self.specialist_email = specialist_email

    def execute(self):
      session = Session()
      specialist = session.query(Specialist).filter_by(email=self.specialist_email).first()
      if not specialist:
        session.close()
        raise SpecialistIsNotRegister()

      specialist = SpecialistJsonSchema().dump(specialist)
      session.close()
      return specialist