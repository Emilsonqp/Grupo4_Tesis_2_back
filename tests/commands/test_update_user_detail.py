from src.commands.signup_user import SignupUser
from src.commands.update_user_detail import UpdateUserDetail
from src.session import Session, engine
from src.models.model import Base
from src.models.user import User
from src.errors.errors import InvalidParams, UserDoesNotExit, UserAlreadyExists
from datetime import datetime


class TestUpdateUserDetail:
    USER_EMAIL = "ln.bello10@uniandes.edu.co"
    USER_DUPLICATE = "other@uniandes.edu.co"

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        data = {
            'name': "Laura",
            'email': self.USER_EMAIL,
            'birth_day': datetime.now().date().isoformat(),
            'city': 'Bogotá',
            'phone': "1234567890",
            'password': "laura"
        }
        self.user = SignupUser(data).execute()

    def test_update_user_no_parameters(self):
        try:
            UpdateUserDetail(self.user['id'], {}).execute()
            assert False
        except InvalidParams:
            assert True

    def test_update_user_not_found(self):
        try:
            UpdateUserDetail(1234567890, {
                'name': 'Laura'
            }).execute()

            assert False
        except UserDoesNotExit:
            assert True

    def test_update_user_duplicate_email(self):
        try:
            SignupUser({
                'name': "Laura",
                'email': self.USER_DUPLICATE,
                'birth_day': datetime.now().date().isoformat(),
                'city': 'Bogotá',
                'phone': "1234567890",
                'password': "laura"
            }).execute()

            UpdateUserDetail(self.user['id'], {
                'email': self.USER_DUPLICATE
            }).execute()

            assert False
        except UserAlreadyExists:
            assert True

    def test_update_user_ok(self):
        UpdateUserDetail(self.user['id'], {
            'name': 'New name'
        }).execute()

        user = self.session.query(User).filter_by(id=self.user['id']).first()
        assert user.name == 'New name'

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)
