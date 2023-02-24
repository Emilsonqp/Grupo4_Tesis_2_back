from datetime import datetime

from src.commands.create_consult import CreateConsult
from src.commands.signup_user import SignupUser
from src.commands.update_consult_status import UpdateConsultStatus
from src.errors.errors import InvalidParams, ConsultDoesNotExist, ConsultWithoutDiagnosis
from src.models.consult import Consult
from src.models.model import Base
from src.session import engine, Session


class TestUpdateConsultStatus:
    USER_NAME = "Laura"
    USER_EMAIL = "ln.bello10@uniandes.edu.co"
    USER_PHONE = "1234567890"
    USER_PASSWORD = "laura"
    BOGOTA = 'Bogotá'
    MEDELLIN = 'Medellin'

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

        data = {
            'name': self.USER_NAME,
            'email': self.USER_EMAIL,
            'birth_day': datetime.now().date().isoformat(),
            'city': self.BOGOTA,
            'phone': self.USER_PHONE,
            'password': self.USER_PASSWORD
        }

        self.user = SignupUser(data).execute()
        self.consult_diagnosis = CreateConsult(self.user['email'], {
            "injury_type": "test",
            "shape": "circular",
            "injuries_count": 1,
            "distribution": "brazo",
            "color": "rojo",
            "photo_url": "https://google.com/",
            "automatic": True,
            "specialist_id": None
        }).execute()

        self.consult_no_diagnosis = CreateConsult(self.user['email'], {
            "injury_type": "test",
            "shape": "circular",
            "injuries_count": 1,
            "distribution": "brazo",
            "color": "rojo",
            "photo_url": "https://google.com/",
            "automatic": False,
            "specialist_id": None
        }).execute()

    def test_update_consult_no_status(self):
        try:
            UpdateConsultStatus(self.consult_diagnosis['id'], {}).execute()

            assert False
        except InvalidParams:
            assert True

    def test_update_consult_invalid_status(self):
        try:
            UpdateConsultStatus(self.consult_diagnosis['id'], {
                "status": 900
            }).execute()

            assert False
        except InvalidParams:
            assert True

    def test_update_consult_invalid_consult(self):
        try:
            UpdateConsultStatus(900, {
                "status": 1
            }).execute()

            assert False
        except ConsultDoesNotExist:
            assert True

    def test_update_consult_invalid_diagnosis(self):
        try:
            UpdateConsultStatus(self.consult_no_diagnosis['id'], {
                "status": 1
            }).execute()

            assert False
        except ConsultWithoutDiagnosis:
            assert True

    def test_update_consult_ok(self):
        consult = UpdateConsultStatus(self.consult_diagnosis['id'], {
            "status": 1
        }).execute()

        updated_consult = self.session.query(Consult).filter_by(id=self.consult_diagnosis['id']).first()
        assert consult['id'] == updated_consult.id

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)
