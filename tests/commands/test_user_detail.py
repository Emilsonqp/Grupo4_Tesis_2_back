from src.commands.signup_user import SignupUser
from src.commands.user_detail import UserDetail
from src.session import Session, engine
from src.models.model import Base
from src.models.user import User
from src.errors.errors import UserDoesNotExit
from datetime import datetime

class TestUserDetail():
  USER_NAME = "Laura"
  USER_EMAIL = "ln.bello10@uniandes.edu.co"
  USER_PHONE = "1234567890"
  USER_PASSWORD = "laura"
  TRUE = True
  FALSE = False
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

  def test_user_detail(self):
    user = UserDetail(self.user['id']).execute()
    assert user['id'] == self.user['id']

  def test_user_detail_does_not_exist(self):
    try:
      UserDetail(2).execute()
      assert self.FALSE
    except UserDoesNotExit:
      assert self.TRUE

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)