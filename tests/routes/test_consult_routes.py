from src.commands.update_consult_status import UpdateConsultStatus
from src.constants import Constants
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
  BASE_PATH = '/consults'

  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.user_data = {
      'name': Utils.USER_NAME,
      'email': Utils.USER_EMAIL,
      'birth_day': datetime.now().date().isoformat(),
      'city': Utils.USER_CITY,
      'phone': Utils.USER_PHONE,
      'password': Utils.USER_PASSWORD
    }
    self.user = SignupUser(self.user_data.copy()).execute()

  def test_create_consult(self):
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
          "automatic": False,
          "specialist_id":  1
        }
        response = test_client.post(
          self.BASE_PATH, json=consult_data,
          headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 201
        assert 'id' in response_json
        assert 'created_at' in response_json

  def test_create_consult_missing_fields(self):
    with app.test_client() as test_client:
      with app.app_context():
        access_token = create_access_token(identity=Utils.USER_EMAIL)
        response = test_client.post(
          self.BASE_PATH, json={},
          headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        json.loads(response.data)
        assert response.status_code == 400

  def test_get_consults(self):
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
          "automatic": False
        }
        CreateConsult(Utils.USER_EMAIL, consult_data).execute()
        response = test_client.get(
          self.BASE_PATH, headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert len(response_json) == 1
        assert 'id' in response_json[0]
        assert 'created_at' in response_json[0]

  def test_get_consult(self):
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
          "automatic": False
        }
        consult = CreateConsult(Utils.USER_EMAIL, consult_data).execute()
        response = test_client.get(
          f"{self.BASE_PATH}/{int(consult['id'])}", headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json
        assert 'created_at' in response_json

  def test_update_consult_status(self):
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
          "automatic": True
        }
        consult = CreateConsult(Utils.USER_EMAIL, consult_data).execute()
        response = test_client.put(
          f"{self.BASE_PATH}/{int(consult['id'])}", headers={
            'Authorization': f"Bearer {access_token}"
          }, json={
            'status': 1
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json
        assert response_json['status'] == 1

  def test_get_pending_consults(self):
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
          "automatic": False
        }
        CreateConsult(Utils.USER_EMAIL, consult_data).execute()
        response = test_client.get(
          '/pending_consults', headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert len(response_json) == 1
        assert 'id' in response_json[0]
        assert 'created_at' in response_json[0]

  def test_get_confirmed_consults(self):
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
          "automatic": True
        }
        consult = CreateConsult(Utils.USER_EMAIL, consult_data).execute()
        consult['status'] = Constants.STATUS_CONFIRMED
        UpdateConsultStatus(consult['id'], consult).execute()
        response = test_client.get(
          '/confirmed_consults', headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 412

  def test_get_consults_by_filters(self):
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
          "automatic": False
        }
        CreateConsult(Utils.USER_EMAIL, consult_data).execute()
        response = test_client.get(
          '/consults_by_filters', headers={
            'Authorization': f"Bearer {access_token}"
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 412

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)