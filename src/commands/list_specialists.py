from .base_command import BaseCommannd
from ..session import Session
from ..models.specialist import Specialist, SpecialistJsonSchema
from ..errors.errors import SpecialistIsNotRegister

class ListSpecialists(BaseCommannd):
    def execute(self):
        session = Session()
        sp = session.query(Specialist).all()
        sp = SpecialistJsonSchema(many=True).dump(sp)
        session.close()

        return sp

class ListSpecialistByEmail(BaseCommannd):
    def __init__(self, sp_email):
        self.sp_email = sp_email

    def execute(self):        
        session = Session()
        sp = session.query(Specialist).filter_by(
            email=self.sp_email).first()        
        if not sp:
            session.close()
            raise SpecialistIsNotRegister()
        
        sp = SpecialistJsonSchema().dump(sp)
        session.close()

        return sp
