from src.session import Session, engine
from src.models.model import Base
from src.main import app
from datetime import datetime
from src.commands.signup_user import SignupUser
from src.commands.create_consult import CreateConsult
from flask_jwt_extended import create_access_token
import json
from tests.utils import Utils

class TestUserRoutes():
  BASE_PATH = '/users'

  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_user(self):
    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH, json={
          'name': Utils.USER_NAME,
          'email': Utils.USER_EMAIL,
          'birth_day': datetime.now().date().isoformat(),
          'city': Utils.USER_CITY,
          'phone': Utils.USER_PHONE,
          'password': Utils.USER_PASSWORD
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
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.USER_CITY,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    SignupUser(data.copy()).execute()

    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH, json=data
      )
      assert response.status_code == 412

  def test_login_user_without_fields(self):
    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH+'/login', json={}
      )
      assert response.status_code == 400

  def test_login_user_invalid_password(self):
    signup_data = {
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.USER_CITY,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    SignupUser(signup_data.copy()).execute()

    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH+'/login', json={
          'email': Utils.USER_EMAIL,
          'password': 'test'
        }
      )
      assert response.status_code == 401

  def test_login_user(self):
    signup_data = {
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.USER_CITY,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    SignupUser(signup_data.copy()).execute()

    with app.test_client() as test_client:
      response = test_client.post(
        self.BASE_PATH + '/login', json={
          'email': Utils.USER_EMAIL,
          'password': Utils.USER_PASSWORD
        }
      )
      response_json = json.loads(response.data)
      assert response.status_code == 201
      assert 'token' in response_json

  def test_update_user_city(self):
    signup_data = {
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.USER_CITY,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    SignupUser(signup_data.copy()).execute()
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.USER_EMAIL)
        response = test_client.put(
          self.BASE_PATH + '/update_city', json={
            'city': Utils.MEDELLIN
          }, headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'city' in response_json

  def test_list_users(self):
    signup_data = {
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.USER_CITY,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    SignupUser(signup_data.copy()).execute()
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.USER_EMAIL)
        response = test_client.get(
          self.BASE_PATH, headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert len(response_json) == 1
        assert 'id' in response_json[0]


  def test_user_detail(self):
    signup_data = {
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.USER_CITY,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    user = SignupUser(signup_data.copy()).execute()
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.USER_EMAIL)
        response = test_client.get(
          self.BASE_PATH + f'/{int(user["id"])}', headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json

  def test_user_detail_doesnt_exist(self):
    signup_data = {
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.USER_CITY,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    user = SignupUser(signup_data.copy()).execute()
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.USER_EMAIL)
        response = test_client.get(
          self.BASE_PATH + f'/10', headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        json.loads(response.data)
        assert response.status_code == 404

  def test_list_user_consults(self):
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.USER_EMAIL)
        consult_data = {
          "injury_type": "test",
          "shape": "circular",
          "injuries_count": 1,
          "distribution": "brazo",
          "color": "rojo",
          "photo_url": "https://google.com/",
          "specialist_id": 1
        }
        signup_data = {
          'name': Utils.USER_NAME,
          'email': Utils.USER_EMAIL,
          'birth_day': datetime.now().date().isoformat(),
          'city': Utils.USER_CITY,
          'phone': Utils.USER_PHONE,
          'password': Utils.USER_PASSWORD
        }
        user = SignupUser(signup_data.copy()).execute()
        CreateConsult(user['email'], consult_data).execute()
        response = test_client.get(
          self.BASE_PATH + f"/{int(user['id'])}/consults", headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json[0]
        assert 'created_at' in response_json[0]

  def test_user_detail_update(self):
    signup_data = {
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.USER_CITY,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    user = SignupUser(signup_data.copy()).execute()
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.USER_EMAIL)
        response = test_client.put(
          self.BASE_PATH + f'/{int(user["id"])}', headers={
            'Authorization': f"Bearer {access_token}"
          }, json={
            'name': Utils.USER_NAME + '_updated'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'name' in response_json
        assert response_json['name'] == Utils.USER_NAME + '_updated'

  def test_user_detail_update_invalid_fields(self):
    signup_data = {
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.USER_CITY,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    user = SignupUser(signup_data.copy()).execute()
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.USER_EMAIL)
        response = test_client.put(
          self.BASE_PATH + f'/{int(user["id"])}', headers={
            'Authorization': f"Bearer {access_token}"
          }, json={
            'another_field': 'test'
          }
        )
        assert response.status_code == 400

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)