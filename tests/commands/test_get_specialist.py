from src.commands.get_specialist import GetSpecialist
from src.commands.signup_specialist import SignupSpecialist
from src.commands.get_consult import GetConsult
from src.session import Session, engine
from src.models.model import Base
from src.errors.errors import SpecialistIsNotRegister
from tests.utils import Utils

class TestGetConsult():
  def setup_method(self):
      Base.metadata.create_all(engine)
      self.session = Session()
      self.specialist = self.create_specialist()

  def test_get_specialist(self):
    specialist = GetSpecialist(self.specialist['id']).execute()
    assert 'id' in specialist

  def test_get_specialist_does_not_exist(self):
    try:
      GetSpecialist(self.specialist['id'] + 1).execute()
      assert False
    except SpecialistIsNotRegister:
      assert True
  
  def create_specialist(self):
    specialist_data = {
      'name': Utils.SPECIALIST_NAME,
      'email': Utils.SPECIALIST_EMAIL,
      'last_name': Utils.SPECIALIST_LAST_NAME,
      'username': Utils.SPECIALIST_USERNAME,
      'password': Utils.SPECIALIST_PASSWORD
    }
    return SignupSpecialist(specialist_data).execute()

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)