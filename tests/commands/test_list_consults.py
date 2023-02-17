
from src.commands.signup_user import SignupUser
from src.commands.signup_specialist import SignupSpecialist
from src.commands.create_consult import CreateConsult
from src.commands.get_agenda import GetAgenda
from src.session import Session, engine
from src.models.model import Base
from src.models.user import User
from src.models.consult import Consult
from src.errors.errors import InvalidParams, InvalidUserCredentials
from datetime import datetime

class TestCreateConsult():
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
      self.data = {
          'name': self.USER_NAME,
          'email': self.USER_EMAIL,
          'birth_day': datetime.now().date().isoformat(),
          'city': self.BOGOTA,
          'phone': self.USER_PHONE,
          'password': self.USER_PASSWORD
      }

      data_specialist = {
        'name': self.USER_NAME,
        'last_name': self.USER_NAME,
        'email': self.USER_EMAIL,
        'username': self.USER_NAME,
        'password': self.USER_PASSWORD
      }
      self.consult_data = {
        "injury_type": "test",
        "shape": "circular",
        "injuries_count": 1,
        "distribution": "brazo",
        "color": "rojo",
        "photo_url": "https://google.com/",
        "specialist_id": 1
      }

      self.specialist = SignupSpecialist(data_specialist).execute()
      self.user = SignupUser(self.data).execute()

  def test_get_consult(self):
    consult = CreateConsult(self.user['email'], self.consult_data).execute()
    x = GetAgenda(self.user['email']).execute()

    assert 'specialist_id' in consult
    assert len(x) == 3

  def test_get_consults_invalid_user(self):
    try:
      CreateConsult('invalid@gmail.com', self.consult_data).execute()
      GetAgenda(self.user['email']).execute()
      assert self.FALSE
    except InvalidUserCredentials:
      consults = self.session.query(Consult).all()
      assert len(consults) == 0
      
  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)