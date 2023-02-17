from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import InvalidParams, InvalidUserCredentials
from ..models.consult import Consult, ConsultJsonSchema
from ..models.specialist import Specialist
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
            
            return ConsultJsonSchema(many=True).dump(consultas)

        except TypeError:
            session.close()
            raise InvalidParams()
        except Exception as error:
            session.close()
            print(error)
            raise error