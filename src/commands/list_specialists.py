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

class ListSpecialistById(BaseCommannd):
    def __init__(self, sp_id):
        self.sp_id = sp_id

    def execute(self):        
        session = Session()
        sp = session.query(Specialist).filter_by(
            id=self.sp_id).first()        
        if not sp:
            session.close()
            raise SpecialistIsNotRegister()
        
        sp = SpecialistJsonSchema().dump(sp)
        session.close()

        return sp
