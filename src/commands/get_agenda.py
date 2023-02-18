from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import InvalidParams, InvalidUserCredentials
from ..models.consult import Consult, ConsultJsonSchema, ConsultJsonSchemaReadable
from ..models.specialist import Specialist
from ..models.user import User
import json
from flask import jsonify
class GetAgenda(BaseCommannd):
    def __init__(self, user_email):
        self.specialist_email = user_email

    def execute(self):
        session = Session()
        try:
            specialist = session.query(Specialist).filter_by(email=self.specialist_email).first()
            if not specialist:
                print(specialist)
                raise InvalidUserCredentials()

            user_id = 1
            consultas = session.query(Consult).filter(Consult.specialist_id==user_id).all()
            session.close()

            response = []
            for consulta in consultas:
                c = ConsultJsonSchemaReadable().dump(consulta)
                print(specialist)
                c["specialist_name"] = specialist.name + " " + specialist.last_name
                u = session.query(User).filter_by(id=consulta.user_id).first() 
                c["user_name"] = u.name
                c["user_email"] = u.email
                response.append(c)

            return response

        except TypeError:
            session.close()
            raise InvalidParams()
        except Exception as error:
            session.close()
            print(error)
            raise error