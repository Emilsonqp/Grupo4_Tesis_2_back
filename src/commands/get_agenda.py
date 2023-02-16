from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import InvalidParams, InvalidUserCredentials
from ..models.consult import Consult, ConsultJsonSchema
from ..models.user import Specialist
import json

class GetAgenda(BaseCommannd):
    def __init__(self, user_email):
        self.specialist_email = user_email

    def execute(self):
        session = Session()
        try:
            user = session.query(Specialist).filter_by(email=self.specialist_email).first()
            if not user:
                print(user)
                raise InvalidUserCredentials()

            user_id = 1
            consultas = session.query(Consult).filter(Consult.specialist_id==user_id).all()
            session.close()
            
            if not consultas:
                return [] 
            return [ConsultJsonSchema().dump(consulta) for consulta in consultas]

        except TypeError:
            session.close()
            raise InvalidParams()
        except Exception as error:
            session.close()
            raise error