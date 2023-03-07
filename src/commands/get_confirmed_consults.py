from ..models.user import User
from ..constants import Constants
from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ConsultDoesNotExist
from ..models.consult import Consult, ConsultJsonSchemaReadable
import json
from flask import jsonify


class GetConfirmedConsults(BaseCommannd):
    def __init__(self, specialist_id):
        self.specialist_id = specialist_id

    def execute(self):
        session = Session()
        consults = session.query(Consult).filter_by(
            status=Constants.STATUS_CONFIRMED, specialist_id=self.specialist_id).all()
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
