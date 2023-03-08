import datetime

from ..models.user import User
from ..constants import Constants
from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ConsultDoesNotExist
from ..models.consult import Consult, ConsultJsonSchemaReadable
import json
from flask import jsonify, request


class GetConsultsByFilters(BaseCommannd):
    def __init__(self, specialist_id):
        self.startDate = request.args.get('startDate') or ''
        self.endDate = request.args.get('endDate') or ''
        self.injury_type = request.args.get('injury_type') or ''
        self.specialist_id = specialist_id

    def execute(self):
        session = Session()
        if ((self.startDate == '') and (self.injury_type == '')):
            consults = session.query(Consult).filter_by(
                status=Constants.STATUS_CONFIRMED, specialist_id=self.specialist_id).all()
        else:
            if (self.startDate != ''):
                if (self.endDate == ''):
                    self.endDate = self.startDate

                if (self.injury_type != ''):
                    consults = session.query(Consult).filter(Consult.updated_at.between(self.toDate(self.startDate), self.toDate(
                        self.endDate)), Consult.injury_type == self.injury_type, Consult.status == Constants.STATUS_CONFIRMED, Consult.specialist_id == self.specialist_id).all()
                else:
                    consults = session.query(Consult).filter(Consult.updated_at.between(self.toDate(self.startDate), self.toDate(
                        self.endDate)), Consult.status == Constants.STATUS_CONFIRMED, Consult.specialist_id == self.specialist_id).all()
            else:
                consults = session.query(Consult).filter_by(
                    injury_type=self.injury_type, status=Constants.STATUS_CONFIRMED, specialist_id=self.specialist_id).all()

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

    def toDate(self, dateString):
        return datetime.datetime.strptime(dateString, "%Y-%m-%d").date()
