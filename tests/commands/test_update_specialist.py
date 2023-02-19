from src.commands.signup_specialist import SignupSpecialist
from src.commands.update_specialist import UpdateSpecialist
from src.session import Session, engine
from src.models.model import Base
from src.models.specialist import Specialist
from src.errors.errors import Unauthorized, InvalidParams, SpecialistAlreadyExists, SpecialistNotMatchPassword
import argon2


class TestUpdateSpecialist():
    SPECIALIST_NAME = "Emilson"
    SPECIALIST_LASTNAME = "Quintero"
    SPECIALIST_EMAIL = "emilsonqp@gmail.com"
    SPECIALIST_EMAIL2 = "emilsonquinterop@gmail.com"
    SPECIALIST_USERNAME = "dquintero"
    SPECIALIST_PWD = "init_pwd"
    TRUE = True
    FALSE = False
    NEW_PASSWORD = "new_password"

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
        self.user = SignupSpecialist(data).execute()
        data['email'] = self.SPECIALIST_EMAIL2
        self.user = SignupSpecialist(data).execute()

    def test_update_specialist_invalid_email(self):
        try:
            UpdateSpecialist(self.SPECIALIST_EMAIL, {
                'email': self.SPECIALIST_EMAIL2
            }).execute()

            assert self.FALSE
        except SpecialistAlreadyExists:
            assert self.TRUE

    def test_update_specialist_invalid_password(self):
        try:
            UpdateSpecialist(self.SPECIALIST_EMAIL, {
                'email': self.SPECIALIST_EMAIL,
                'password': self.SPECIALIST_PWD,
                're_password': "another_password"
            }).execute()

            assert self.FALSE
        except SpecialistNotMatchPassword:
            assert self.TRUE

    def test_update_specialist_not_found(self):
        try:
            UpdateSpecialist("another_email@gmail.com", {
                'email': "another_email@gmail.com",
                'password': self.SPECIALIST_PWD,
                're_password': self.SPECIALIST_PWD
            }).execute()

            assert self.FALSE
        except Unauthorized:
            assert self.TRUE

    def test_update_specialist(self):
        ph = argon2.PasswordHasher()
        UpdateSpecialist(self.SPECIALIST_EMAIL, {
            'name': self.SPECIALIST_NAME,
            'email': self.SPECIALIST_EMAIL,
            'last_name': self.SPECIALIST_LASTNAME,
            'username': self.SPECIALIST_USERNAME,
            'password': self.NEW_PASSWORD,
            're_password': self.NEW_PASSWORD
        }).execute()

        sp = self.session.query(Specialist).filter_by(
            email=self.SPECIALIST_EMAIL).first()
        pass_hash = sp.password
        assert ph.verify(pass_hash, self.NEW_PASSWORD.encode('utf-8'))

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)
