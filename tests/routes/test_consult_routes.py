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
          "photo_url": "https://google.com/"
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

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)