from src.session import Session, engine
from src.models.model import Base
from src.main import app
from datetime import datetime
from src.commands.signup_user import SignupUser
import json

class TestUserRoutes():
  USER_NAME = "William"
  USER_EMAIL = "wr.ravelo@uniandes.edu.co"
  USER_CITY = "Bogotá"
  USER_PHONE = "12312412"
  USER_PASSWORD = "123456"
  BASE_PATH = '/users'

  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_user(self):
    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH, json={
          'name': self.USER_NAME,
          'email': self.USER_EMAIL,
          'birth_day': datetime.now().date().isoformat(),
          'city': self.USER_CITY,
          'phone': self.USER_PHONE,
          'password': self.USER_PASSWORD
        }
      )
      response_json = json.loads(response.data)
      assert response.status_code == 201
      assert 'name' in response_json
      assert 'email' in response_json
      assert 'token' in response_json
      assert 'password' not in response_json

  def test_create_user_missing_fields(self):
    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH, json={}
      )
      assert response.status_code == 400

  def test_create_existing_email(self):
    data = {
      'name': self.USER_NAME,
      'email': self.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': self.USER_CITY,
      'phone': self.USER_PHONE,
      'password': self.USER_PASSWORD
    }
    SignupUser(data.copy()).execute()

    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH, json=data
      )
      assert response.status_code == 412

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)