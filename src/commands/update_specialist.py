from .base_command import BaseCommannd
from ..models.specialist import Specialist, SpecialistJsonSchema
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
      if (self.sp_email != self.data['email']):
        if self.email_exist(session, self.data['email']):
          session.close()
          raise SpecialistAlreadyExists()

      pwd_to_change = self.data['password'].replace(" ", "")
      if len(pwd_to_change) > 0 or len(self.data['re_password'].replace(" ", "")):
        if (pwd_to_change != self.data['re_password'].replace(" ", "")):
          session.close()
          raise SpecialistNotMatchPassword()
  
      specialist = session.query(Specialist).filter_by(email=self.sp_email).first()

      if specialist is None:
        session.close()
        raise Unauthorized()
      
      if specialist.name != self.data['name'] : specialist.name = self.data['name']
      if specialist.last_name != self.data['last_name'] : specialist.last_name = self.data['last_name']
      if specialist.email != self.data['email'] : specialist.email = self.data['email']
      if specialist.username != self.data['username'] : specialist.username = self.data['username']
      pass_hash = specialist.password
      if len(pwd_to_change) > 0 : ph.verify(pass_hash, pwd_to_change.encode('utf-8'))
      session.commit()

      specialist = SpecialistJsonSchema().dump(specialist)
      session.close()

      return specialist
    except TypeError:
      raise InvalidParams()
    except (argon2.exceptions.VerifyMismatchError, argon2.exceptions.VerificationError, argon2.exceptions.InvalidHash):
      specialist.password = ph.hash(pwd_to_change.encode('utf-8'))
      session.commit()
      
      specialist = SpecialistJsonSchema().dump(specialist)
      session.close()
      return specialist
    except Exception as error:
      session.close()
      raise error
    
  def email_exist(self, session, email):
    return len(session.query(Specialist).filter_by(email=email).all()) > 0    
