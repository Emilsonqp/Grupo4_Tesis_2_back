from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import InvalidParams, InvalidUserCredentials
from ..models.consult import Consult, ConsultSchema, ConsultJsonSchema
from ..models.user import User

class CreateConsult(BaseCommannd):
    def __init__(self, user_email, data):
        self.user_email = user_email
        self.data = data

    def execute(self):
        session = Session()
        try:
            user = session.query(User).filter_by(email=self.user_email).first()
            if not user:
                print(user)
                raise InvalidUserCredentials()

            self.data['user_id'] = user.id
            
            print(self.data)
            posted_consult = ConsultSchema(
                only=("injury_type", "shape", "injuries_count", "distribution", "color", "photo_url", "user_id", "specialist_id")
            ).load(self.data)
            consult = Consult(**posted_consult)
            session.add(consult)
            session.commit()

            new_consult = ConsultJsonSchema().dump(consult)
            session.close()

            return new_consult
        except TypeError as e:
            print(e)
            session.close()
            raise InvalidParams()
        except Exception as error:
            print(error)
            session.close()
            raise error