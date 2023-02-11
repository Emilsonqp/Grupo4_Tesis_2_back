from .base_command import BaseCommannd
from ..models.specialist import Specialist
from ..session import Session
from ..errors.errors import InvalidParams, SpecialistIsNotRegister, SpecialistWrongPassword

class UserDetail(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
      print("Initial")