from src.session import Session, engine
from src.models.model import Base
from src.main import app
from datetime import datetime
from src.commands.signup_specialist import SignupSpecialist
from sqlalchemy.orm import close_all_sessions
import json
import string
import random

class TestUserRoutes():
  SPECIALIST_NAME = "Pedro"
  SPECIALIST_EMAIL = "pedro@gmail.com"
  SPECIALIST_LAST_NAME = "Cabra"
  SPECIALIST_USERNAME = "p.cabra"
  SPECIALIST_PASSWORD = "123456"
  BASE_PATH = '/specialist'
  letters = string.ascii_lowercase
  LOGIN_BASE_PATH = '/login'

  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_specialist(self):
    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH, json={
          'name': self.SPECIALIST_NAME,
          'email': self.SPECIALIST_EMAIL,
          'last_name': self.SPECIALIST_LAST_NAME,
          'username': self.SPECIALIST_USERNAME,
          'password': self.SPECIALIST_PASSWORD
        }
      )
      response_json = json.loads(response.data)
      assert response.status_code == 201
      assert 'name' in response_json
      assert 'email' in response_json
      assert 'token' in response_json

  def test_create_user_missing_fields(self):
    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH, json={}
      )
      assert response.status_code == 400

  def test_create_existing_email(self):
    data = {
      "name": self.SPECIALIST_NAME,
          'email': self.SPECIALIST_EMAIL,
          'last_name': self.SPECIALIST_LAST_NAME,
          'username': self.SPECIALIST_USERNAME,
          'password': self.SPECIALIST_PASSWORD
    }
    SignupSpecialist(data.copy()).execute()

    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH, json=data
      )
      assert response.status_code == 412
  
  def test_login_specialist(self):
    signup_data = {
      'name': self.SPECIALIST_NAME,
      'email': self.SPECIALIST_EMAIL,
      'last_name': self.SPECIALIST_LAST_NAME,
      'username': self.SPECIALIST_USERNAME,
      'password': self.SPECIALIST_PASSWORD
    }
    SignupSpecialist(signup_data.copy()).execute()

    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH + self.LOGIN_BASE_PATH, json={
          'email': self.SPECIALIST_EMAIL,
          'password': self.SPECIALIST_PASSWORD
        }
      )
      response_json = json.loads(response.data)
      assert response.status_code == 201
      assert 'access_token' in response_json

  def test_login_specialist_without_fields(self):
    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH+self.LOGIN_BASE_PATH, json={}
      )
      assert response.status_code == 400

  def test_login_specialist_invalid_password(self):
    signup_data = {
      'name': self.SPECIALIST_NAME,
      'email': self.SPECIALIST_EMAIL,
      'last_name': self.SPECIALIST_LAST_NAME,
      'username': self.SPECIALIST_USERNAME,
      'password': self.SPECIALIST_PASSWORD
    }
    SignupSpecialist(signup_data.copy()).execute()

    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH + self.LOGIN_BASE_PATH, json={
          'email': self.SPECIALIST_EMAIL,
          'password': ''.join(random.choice(self.letters) for _ in range(5))
        }
      )
      assert response.status_code == 401

  def teardown_method(self):
    close_all_sessions()
    Base.metadata.drop_all(bind=engine)