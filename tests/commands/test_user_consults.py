from src.commands.signup_user import SignupUser
from src.commands.create_consult import CreateConsult
from src.commands.user_consults import UserConsults
from src.session import Session, engine
from src.models.model import Base
from src.models.user import User
from src.models.consult import Consult
from src.errors.errors import InvalidParams, InvalidUserCredentials
from datetime import datetime

class TestUserConsults():
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
      self.consult_data = {
        "injury_type": "test",
        "shape": "circular",
        "injuries_count": 1,
        "distribution": "brazo",
        "color": "rojo",
        "photo_url": "https://google.com/",
        "automatic": False,
        "specialist_id": None
      }
      self.user = SignupUser(data).execute()
      self.consult = CreateConsult(self.user['email'], self.consult_data).execute()

  def test_list_consults(self):
    consults = UserConsults(self.user['id']).execute()
    assert len(consults) == 1
    assert 'id' in consults[0]

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)