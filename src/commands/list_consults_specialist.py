from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import InvalidParams, InvalidUserCredentials
from ..models.consult import Consult, ConsultJsonSchema, ConsultJsonSchemaReadable
from ..models.specialist import Specialist
from ..models.user import User
import json
from flask import jsonify
class ConsultSpecialistUpdate(BaseCommannd):
    def __init__(self, user_email, id, description, diagnosis ):
        self.specialist_email = user_email
        self.consult_id = id
        self.description = description
        self.diagnosis = diagnosis

    def execute(self):
        session = Session()
        try:
            print(self.specialist_email)
            specialist = session.query(Specialist).filter_by(email=self.specialist_email).first()
            if not specialist:
                print(specialist)
                raise InvalidUserCredentials()

            consulta = session.query(Consult).filter_by(id=self.consult_id).first()

            consulta.diagnosis = self.diagnosis
            consulta.description = self.description
            consulta.status = 1
            
            session.commit()
            session.close()
            return "ok"

        except TypeError:
            session.close()
            raise InvalidParams()
        except Exception as error:
            session.close()
            print(error)
            raise error