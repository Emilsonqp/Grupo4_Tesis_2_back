from src.commands.signup_user import SignupUser
from src.commands.update_user_city import UpdateUserCity
from src.session import Session, engine
from src.models.model import Base
from src.models.user import User
from src.errors.errors import Unauthorized, InvalidParams
from datetime import datetime

class TestUpdateCity():
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

  def test_update_city_missing_parameters(self):
    try:
      UpdateUserCity(self.USER_EMAIL, {}).execute()

      assert self.FALSE
    except InvalidParams:
      assert self.TRUE
  
  def test_update_city_invalid_user(self):
    try:
      UpdateUserCity("fake@gmail.com", {
        'city': self.MEDELLIN
      }).execute()

      assert self.FALSE
    except Unauthorized:
      assert self.TRUE

  def test_update_city(self):
    UpdateUserCity(self.USER_EMAIL, {
        'city': self.MEDELLIN
      }).execute()
    
    user = self.session.query(User).filter_by(email=self.USER_EMAIL).first()
    assert user.city == self.MEDELLIN

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)