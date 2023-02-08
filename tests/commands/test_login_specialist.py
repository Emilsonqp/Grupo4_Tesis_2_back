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
from src.main import app

class TestLoginSpecialist():
  SPECIALIST_NAME = "Pedro"
  SPECIALIST_EMAIL = "pedro@gmail.com"
  SPECIALIST_LAST_NAME = "Cabra"
  SPECIALIST_USERNAME = "p.cabra"
  SPECIALIST_PASSWORD = "123456"
  BASE_PATH = '/specialist/login'
  letters = string.ascii_lowercase
  SUCCESS_TRUE = True

  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.new_sp_email = ''.join(random.choice(self.letters) for _ in range(10)) + "@uniandes.edu.co"

    data = {
      'name': self.SPECIALIST_NAME,
      'email': self.SPECIALIST_EMAIL,
      'last_name': self.SPECIALIST_LAST_NAME,
      'username': self.SPECIALIST_USERNAME,
      'password': self.SPECIALIST_PASSWORD
    }
    self.user= SignupSpecialist(data).execute()

  def test_login_specialist(self):
    sp = {
      'email': self.SPECIALIST_EMAIL,
      'password': self.SPECIALIST_PASSWORD
    }
    try:
      with app.app_context():
        specialist = LoginSpecialist(sp).execute()

      assert len(specialist['access_token']) > 0
    except SpecialistIsNotRegister:
      assert self.SUCCESS_TRUE

  def test_login_specialist_missing_fields(self):
    try:
      LoginSpecialist({}).execute()

      assert False
    except InvalidParams:
      assert self.SUCCESS_TRUE

  def test_login_specialist_not_register(self):
    try:
      sp = {
       'email': ''.join(random.choice(self.letters) for _ in range(10)) + "@uniandes.edu.co",
       'password': self.SPECIALIST_PASSWORD
      }
      LoginSpecialist(sp).execute()

      assert False
    except SpecialistIsNotRegister:
      assert self.SUCCESS_TRUE

  def test_login_specialist_wrong_password(self):
    sp = {
      'email': self.SPECIALIST_EMAIL,
      'password': ''.join(random.choice(self.letters) for _ in range(5))
     }
    try:
      LoginSpecialist(sp).execute()

      assert False
    except SpecialistWrongPassword:
      assert self.SUCCESS_TRUE

  def teardown_method(self):
    close_all_sessions()
    Base.metadata.drop_all(bind=engine)