from src.session import Session, engine
from src.models.model import Base
from src.main import app
from datetime import datetime
from src.commands.signup_specialist import SignupSpecialist
from sqlalchemy.orm import close_all_sessions
import json
import string
import random
from flask_jwt_extended import create_access_token
from tests.utils import Utils

class TestUserRoutes():
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
          'name': Utils.SPECIALIST_NAME,
          'email': Utils.SPECIALIST_EMAIL,
          'last_name': Utils.SPECIALIST_LAST_NAME,
          'username': Utils.SPECIALIST_USERNAME,
          'password': Utils.SPECIALIST_PASSWORD
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
      "name": Utils.SPECIALIST_NAME,
          'email': Utils.SPECIALIST_EMAIL,
          'last_name': Utils.SPECIALIST_LAST_NAME,
          'username': Utils.SPECIALIST_USERNAME,
          'password': Utils.SPECIALIST_PASSWORD
    }
    SignupSpecialist(data.copy()).execute()

    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH, json=data
      )
      assert response.status_code == 412
  
  def test_login_specialist(self):
    signup_data = {
      'name': Utils.SPECIALIST_NAME,
      'email': Utils.SPECIALIST_EMAIL,
      'last_name': Utils.SPECIALIST_LAST_NAME,
      'username': Utils.SPECIALIST_USERNAME,
      'password': Utils.SPECIALIST_PASSWORD
    }
    SignupSpecialist(signup_data.copy()).execute()

    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH + self.LOGIN_BASE_PATH, json={
          'email': Utils.SPECIALIST_EMAIL,
          'password': Utils.SPECIALIST_PASSWORD
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
      'name': Utils.SPECIALIST_NAME,
      'email': Utils.SPECIALIST_EMAIL,
      'last_name': Utils.SPECIALIST_LAST_NAME,
      'username': Utils.SPECIALIST_USERNAME,
      'password': Utils.SPECIALIST_PASSWORD
    }
    SignupSpecialist(signup_data.copy()).execute()

    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH + self.LOGIN_BASE_PATH, json={
          'email': Utils.SPECIALIST_EMAIL,
          'password': ''.join(random.choice(self.letters) for _ in range(5))
        }
      )
      assert response.status_code == 401

  def test_update_specialist(self):
    signup_data = {
      'name': Utils.SPECIALIST_NAME,
      'email': Utils.SPECIALIST_EMAIL,
      'last_name': Utils.SPECIALIST_LAST_NAME,
      'username': Utils.SPECIALIST_USERNAME,
      'password': Utils.SPECIALIST_PASSWORD
    }
    SignupSpecialist(signup_data.copy()).execute()
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.SPECIALIST_EMAIL)
        response = test_client.put(
          self.BASE_PATH + '/update_profile', json={
            'name': Utils.SPECIALIST_NAME,
            'email': Utils.SPECIALIST_EMAIL,
            'last_name': Utils.SPECIALIST_LAST_NAME,
            'username': Utils.SPECIALIST_USERNAME,
            'password': Utils.SPECIALIST_NEWPASSWORD,
            're_password': Utils.SPECIALIST_NEWPASSWORD
          }, headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'token' in response_json

  def test_list_specialist_detail(self):
    signup_data = {
      'name': Utils.SPECIALIST_NAME,
      'email': Utils.SPECIALIST_EMAIL,
      'last_name': Utils.SPECIALIST_LAST_NAME,
      'username': Utils.SPECIALIST_USERNAME,
      'password': Utils.SPECIALIST_PASSWORD
    }
    sp = SignupSpecialist(signup_data.copy()).execute()
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.SPECIALIST_EMAIL)
        response = test_client.get(
          self.BASE_PATH + '/profile' + f'/{int(sp["id"])}', headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json

  def test_take_consults_by_specialist(self):
    signup_data = {
      'name': Utils.SPECIALIST_NAME,
      'email': Utils.SPECIALIST_EMAIL,
      'last_name': Utils.SPECIALIST_LAST_NAME,
      'username': Utils.SPECIALIST_USERNAME,
      'password': Utils.SPECIALIST_PASSWORD
    }
    SignupSpecialist(signup_data.copy()).execute()
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.SPECIALIST_EMAIL)
        response = test_client.post(
          self.BASE_PATH + '/take_consults', json={
            'id_consults': []
          }, headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        assert response.status_code == 400

  def teardown_method(self):
    close_all_sessions()
    Base.metadata.drop_all(bind=engine)