from src.commands.base_command import BaseCommannd
from src.constants import Constants
from src.errors.errors import InvalidParams, ConsultDoesNotExist, ConsultWithoutDiagnosis
from src.models.consult import Consult, ConsultJsonSchema
from src.session import Session


class UpdateConsultStatus(BaseCommannd):

    def __init__(self, consult_id, data):
        self.consult_id = consult_id
        self.data = data

    def execute(self):
        if 'status' not in self.data:
            raise InvalidParams()

        if self.data['status'] not in [Constants.STATUS_PENDING, Constants.STATUS_CONFIRMED, Constants.STATUS_REJECTED]:
            raise InvalidParams()

        session = Session()
        consult = session.query(Consult).filter_by(id=self.consult_id).first()

        if not consult:
            session.close()
            raise ConsultDoesNotExist()

        if not consult.diagnosis:
            session.close()
            raise ConsultWithoutDiagnosis()

        consult.status = self.data['status']
        session.commit()

        consult = ConsultJsonSchema().dump(consult)
        session.close()

        return consult

