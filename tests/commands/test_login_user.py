from src.commands.login_user import LoginUser
from src.commands.signup_user import SignupUser
from src.main import app
from src.session import Session, engine
from src.models.model import Base
from src.errors.errors import InvalidParams, InvalidUserCredentials
from datetime import datetime


class TestLoginUser:
    USER_NAME = "Laura"
    USER_EMAIL = "ln.bello10@uniandes.edu.co"
    USER_CITY = "Bogotá"
    USER_PHONE = "1234567890"
    USER_PASSWORD = "laura"

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

        data = {
            'name': self.USER_NAME,
            'email': self.USER_EMAIL,
            'birth_day': datetime.now().date().isoformat(),
            'city': self.USER_CITY,
            'phone': self.USER_PHONE,
            'password': self.USER_PASSWORD
        }
        self.user = SignupUser(data).execute()

    def test_login_user_missing_fields(self):
        try:
            LoginUser({}).execute()
            assert False
        except InvalidParams:
            assert True

    def test_login_user_invalid_password(self):
        data = {
            'email': self.USER_EMAIL,
            'password': 'test'
        }

        try:
            LoginUser(data).execute()
            assert False
        except InvalidUserCredentials:
            assert True


    def test_login_user_no_user_found(self):
        data = {
            'email': 'test',
            'password': self.USER_PASSWORD
        }

        try:
            LoginUser(data).execute()
            assert False
        except InvalidUserCredentials:
            assert True

    def test_login_user(self):
        data = {
            'email': self.USER_EMAIL,
            'password': self.USER_PASSWORD
        }
        with app.app_context():
            data = LoginUser(data).execute()

        assert len(data['token']) > 0

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)