from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ConsultDoesNotExist
from ..models.consult import Consult, ConsultJsonSchema
from ..commands.get_specialist import GetSpecialist
import json
from flask import jsonify

class GetConsult(BaseCommannd):
  def __init__(self, consult_id):
      self.consult_id = consult_id

  def execute(self):
    session = Session()
    consult = session.query(Consult).filter_by(id=self.consult_id).first()
    if not consult:
      session.close()
      raise ConsultDoesNotExist()

    consult = ConsultJsonSchema().dump(consult)
    if consult['specialist_id'] != None:
      specialist = GetSpecialist(consult['specialist_id']).execute()
      consult['specialist'] = specialist
    else:
      consult['specialist'] = None

    session.close()
    return consult