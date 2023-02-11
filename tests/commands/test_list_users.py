from src.commands.signup_user import SignupUser
from src.commands.list_users import ListUsers
from src.session import Session, engine
from src.models.model import Base
from src.models.user import User
from src.errors.errors import Unauthorized, InvalidParams
from datetime import datetime

class TestListUsers():
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

  def test_list_users(self):
    users = ListUsers().execute()
    assert len(users) == 1
    assert users[0]['id'] == self.user['id']

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)