import json
from flask import jsonify
from src.commands.get_confirmed_consults import GetConfirmedConsults
from src.commands.signup_user import SignupUser
from src.commands.create_consult import CreateConsult
from src.commands.signup_specialist import SignupSpecialist
from src.commands.get_consult import GetConsult, GetPendingConsults
from src.commands.take_consults_by_specialist import TakeConsults
from src.commands.update_consult_status import UpdateConsultStatus
from src.constants import Constants
from src.session import Session, engine
from src.models.model import Base
from src.models.user import User
from src.models.consult import Consult
from src.errors.errors import ConsultDoesNotExist, InvalidParams
from datetime import datetime
from tests.utils import Utils


class TestTakeConsults():
    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def test_take_consults(self):
        try:
            user = self.create_user()
            specialist = self.create_specialist()
            consult = self.create_pending_consult(
                user['email'], specialist['id'])
            consults_to_take = {
                'id_consults': [str(int(consult['id']))]
            }
            print(consults_to_take)
            response = TakeConsults(
                specialist['id'], consults_to_take).execute()
            assert True
        except InvalidParams:
            assert False

    def test_take_consult_without_consults(self):
        try:
            user = self.create_user()
            specialist = self.create_specialist()
            consult = self.create_pending_consult(
                user['email'], specialist['id'])
            consults_to_take = {
                'id_consults': []
            }
            TakeConsults(specialist['id'], consults_to_take).execute()
            assert False
        except InvalidParams:
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

    def create_pending_consult(self, user_email, specialist_id):
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
