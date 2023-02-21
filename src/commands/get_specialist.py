from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import InvalidParams, InvalidUserCredentials, SpecialistIsNotRegister
from ..models.consult import Consult, ConsultJsonSchema, ConsultJsonSchemaReadable
from ..models.specialist import Specialist, SpecialistJsonSchema
from ..models.user import User
import json
from flask import jsonify

class GetSpecialist(BaseCommannd):
  def __init__(self, specialist_id):
      self.specialist_id = specialist_id

  def execute(self):
    session = Session()
    specialist = session.query(Specialist).filter_by(id=self.specialist_id).first()
    if not specialist:
      session.close()
      raise SpecialistIsNotRegister()

    specialist = SpecialistJsonSchema().dump(specialist)
    session.close()
    return specialist