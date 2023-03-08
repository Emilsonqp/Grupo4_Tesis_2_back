from src.commands.get_confirmed_consults import GetConfirmedConsults
from src.commands.signup_user import SignupUser
from src.commands.create_consult import CreateConsult
from src.commands.signup_specialist import SignupSpecialist
from src.commands.get_consult import GetConsult, GetPendingConsults
from src.commands.update_consult_status import UpdateConsultStatus
from src.constants import Constants
from src.session import Session, engine
from src.models.model import Base
from src.models.user import User
from src.models.consult import Consult
from src.errors.errors import ConsultDoesNotExist
from datetime import datetime
from tests.utils import Utils

class TestGetConfirmedConsults():
  def setup_method(self):
      Base.metadata.create_all(engine)
      self.session = Session()

  def test_get_consult_with_specialist(self):
    try:
      user = self.create_user()
      specialist = self.create_specialist()
      consult = self.create_confirmed_consult(user['email'], specialist['id'])
      consult['status'] = Constants.STATUS_CONFIRMED
      consult = UpdateConsultStatus(consult['id'], consult).execute()
      GetConfirmedConsults(specialist['id']).execute()
      assert True
    except ConsultDoesNotExist:
      assert False

  def test_get_consult_does_not_exist(self):
    try:
      user = self.create_user()
      specialist = self.create_specialist()
      consult = self.create_confirmed_consult(user['email'], None)
      GetConfirmedConsults(specialist['id'] + 1).execute()
      assert False
    except ConsultDoesNotExist:
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
  
  def create_specialist(self):
    specialist_data = {
      'name': Utils.SPECIALIST_NAME,
      'email': Utils.SPECIALIST_EMAIL,
      'last_name': Utils.SPECIALIST_LAST_NAME,
      'username': Utils.SPECIALIST_USERNAME,
      'password': Utils.SPECIALIST_PASSWORD
    }
    return SignupSpecialist(specialist_data).execute()

  def create_confirmed_consult(self, user_email, specialist_id):
    consult_data = {
      "injury_type": "test",
      "shape": "circular",
      "injuries_count": 1,
      "distribution": "brazo",
      "color": "rojo",
      "photo_url": "https://google.com/",
      "automatic": True,
      "specialist_id": specialist_id
    }
    return CreateConsult(user_email, consult_data).execute()

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)