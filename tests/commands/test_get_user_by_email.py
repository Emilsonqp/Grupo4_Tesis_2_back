from src.commands.get_specialist import GetSpecialist
from src.commands.signup_user import SignupUser
from src.commands.get_consult import GetConsult
from src.commands.get_user_by_email import GetUserByEmail
from src.session import Session, engine
from src.models.model import Base
from src.errors.errors import InvalidUserCredentials
from tests.utils import Utils
from datetime import datetime

class TestGetUserByEmail():
  def setup_method(self):
      Base.metadata.create_all(engine)
      self.session = Session()
      self.user = self.create_user()

  def test_get_user_by_email(self):
    user = GetUserByEmail(self.user['email']).execute()
    assert 'id' in user
    assert 'email' in user

  def test_get_user_by_email_does_not_exist(self):
    try:
      GetUserByEmail("fake@gmail.com").execute()
      assert False
    except InvalidUserCredentials:
      assert True
  
  def create_user(self):
    user_data = {
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.BOGOTA,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    return SignupUser(user_data).execute()

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)