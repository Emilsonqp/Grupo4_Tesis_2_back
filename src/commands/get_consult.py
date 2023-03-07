from ..constants import Constants
from ..models.user import User
from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ConsultDoesNotExist
from ..models.consult import Consult, ConsultJsonSchema, ConsultJsonSchemaReadable
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


class GetPendingConsults(BaseCommannd):
    def execute(self):
        session = Session()
        consults = session.query(Consult).filter_by(status=Constants.STATUS_PENDING, specialist_id=None, automatic=False).all()
        if not consults:
            session.close()
            raise ConsultDoesNotExist()
        
        response = []
        for consult in consults:
            c = ConsultJsonSchemaReadable().dump(consult)
            u = session.query(User).filter_by(id=consult.user_id).first() 
            c["user_name"] = u.name
            c["user_email"] = u.email
            response.append(c)
        
        session.close()
        return response
