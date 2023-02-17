from src.commands.signup_specialist import SignupSpecialist
from src.commands.list_specialists import ListSpecialistById
from src.session import Session, engine
from src.models.model import Base
from src.models.specialist import Specialist
from src.errors.errors import SpecialistIsNotRegister
from datetime import datetime


class TestListSpecialist():
    SPECIALIST_NAME = "Emilson"
    SPECIALIST_LASTNAME = "Quintero"
    SPECIALIST_EMAIL = "emilsonqp@gmail.com"
    SPECIALIST_EMAIL2 = "emilsonquinterop@gmail.com"
    SPECIALIST_USERNAME = "dquintero"
    SPECIALIST_PWD = "init_pwd"
    TRUE = True
    FALSE = False

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        data = {
            'name': self.SPECIALIST_NAME,
            'email': self.SPECIALIST_EMAIL,
            'last_name': self.SPECIALIST_LASTNAME,
            'username': self.SPECIALIST_USERNAME,
            'password': self.SPECIALIST_PWD
        }
        self.sp = SignupSpecialist(data).execute()

    def test_list_specialist(self):
        sp = ListSpecialistById(self.sp['id']).execute()
        assert sp['id'] == self.sp['id']

    def test_list_specialist_does_not_exist(self):
        try:
            ListSpecialistById(100).execute()
            assert self.FALSE
        except SpecialistIsNotRegister:
            assert self.TRUE

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)
