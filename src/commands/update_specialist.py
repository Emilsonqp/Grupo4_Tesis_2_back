from .base_command import BaseCommannd
from ..models.specialist import Specialist, SpecialistSchema, SpecialistJsonSchema
from ..session import Session
from ..errors.errors import InvalidParams, SpecialistAlreadyExists, Unauthorized, SpecialistNotMatchPassword
import argon2

class UpdateSpecialist(BaseCommannd):
  def __init__(self, sp_email, data):
    self.sp_email = sp_email
    self.data = data
  
  def execute(self):
    session = Session()
    ph = argon2.PasswordHasher()
    try:
      if 'email' not in self.data:
        raise InvalidParams()
    
      if (self.sp_email != self.data['email']):
        if self.email_exist(session, self.data['email']):
          session.close()
          raise SpecialistAlreadyExists()
        
      if (self.data['password'] != self.data['re_password']):
        session.close()
        raise SpecialistNotMatchPassword()
  
      specialist = session.query(Specialist).filter_by(email=self.sp_email).first()

      if specialist is None:
        session.close()
        raise Unauthorized()
      
      specialist.name = self.data['name']
      specialist.last_name = self.data['last_name']
      specialist.email = self.data['email']
      specialist.username = self.data['username']
      specialist.password = ph.hash(self.data['password'].encode('utf-8'))
      session.commit()

      specialist = SpecialistJsonSchema().dump(specialist)
      session.close()

      return specialist
    except TypeError:
      raise InvalidParams()
    except Exception as error:
      session.close()
      raise error
    
  def email_exist(self, session, email):
    return len(session.query(Specialist).filter_by(email=email).all()) > 0    
