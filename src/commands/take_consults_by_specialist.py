import json

from flask import jsonify

from ..models.consult import Consult
from .base_command import BaseCommannd
from ..models.specialist import Specialist, SpecialistJsonSchema
from ..session import Session
from ..errors.errors import InvalidParams, SpecialistAlreadyExists, Unauthorized, SpecialistNotMatchPassword
import argon2

class TakeConsults(BaseCommannd):
  def __init__(self, specialist_id, data):
    self.specialist_id = specialist_id
    self.data = data
  
  def execute(self):
    session = Session()
    try:
      if (len(self.data['id_consults']) == 0):
          session.close()
          raise TypeError()
      
      for idCase in self.data['id_consults']:
        print(idCase)
        consult = session.query(Consult).filter_by(id=idCase).first()
        consult.specialist_id = self.specialist_id
        
      session.commit()
      session.close()

      return {"mssg": "success"}
    except (Exception, TypeError):
      session.close()
      raise InvalidParams()