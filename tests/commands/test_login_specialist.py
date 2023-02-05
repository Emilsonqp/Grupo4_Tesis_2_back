from src.commands.login_specialist import LoginSpecialist
from src.commands.signup_specialist import SignupSpecialist
from src.session import Session, engine
from src.models.model import Base
from src.models.specialist import Specialist
from src.errors.errors import SpecialistIsNotRegister, SpecialistWrongPassword, InvalidParams
from datetime import datetime
from sqlalchemy.orm import close_all_sessions
import string
import random

class TestLoginSpecialist():
  SPECIALIST_NAME = "quinteroe"
  SPECIALIST_EMAIL = "e.quinterop@uniandes.edu.co"
  SPECIALIST_CITY = "Bogotá"
  SPECIALIST_PHONE = "3112221212"
  SPECIALIST_PASSWORD = "miso"
  SPECIALIST_SPECIALITY = "rostro"
  BASE_PATH = '/specialist/login'
  letters = string.ascii_lowercase

  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.new_sp_email = ''.join(random.choice(self.letters) for _ in range(10)) + "@uniandes.edu.co"

    data = {
      'name': self.SPECIALIST_NAME,
      'email': self.new_sp_email,
      'birth_day': datetime.now().date().isoformat(),
      'city': self.SPECIALIST_CITY,
      'phone': self.SPECIALIST_PHONE,
      'password': self.SPECIALIST_PASSWORD,
      'specialty': self.SPECIALIST_SPECIALITY
    }
    self.user= SignupSpecialist(data).execute()

  def test_login_specialist(self):
    sp = {
      'email': self.SPECIALIST_EMAIL,
      'password': self.SPECIALIST_PASSWORD
    }
    try:
      specialist = LoginSpecialist(sp).execute()

      assert specialist['email'] == sp['email']
      assert specialist['password'] == sp['password']
    except SpecialistIsNotRegister:
      assert True

  def test_login_specialist_missing_fields(self):
    try:
      LoginSpecialist({}).execute()

      assert False
    except InvalidParams:
      assert True

  def test_login_specialist_not_register(self):
    try:
      sp = {
       'email': ''.join(random.choice(self.letters) for _ in range(10)) + "@uniandes.edu.co",
       'password': self.SPECIALIST_PASSWORD
      }
      LoginSpecialist(sp).execute()

      assert False
    except SpecialistIsNotRegister:
      assert True

  def test_login_specialist_wrong_password(self):
    sp = {
      'email': self.new_sp_email,
      'password': ''.join(random.choice(self.letters) for i in range(5))
     }
    try:
      LoginSpecialist(sp).execute()

      assert False
    except SpecialistWrongPassword:
      assert True

  def teardown_method(self):
    close_all_sessions()
    Base.metadata.drop_all(bind=engine)