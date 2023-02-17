from datetime import datetime

from src.commands.base_command import BaseCommannd
from src.errors.errors import UserDoesNotExit, UserAlreadyExists, InvalidParams
from src.models.user import User, UserJsonSchema
from src.session import Session
from validx import Dict, Str, exc

validate_user_detail_update = Dict(
    {
        'name': Str(minlen=1),
        'email': Str(minlen=1),
        'birth_day': Str(minlen=1),
        'city': Str(minlen=1),
        'phone': Str(minlen=1),
    },
    optional=['name', 'email', 'birth_day', 'city', 'phone'],
    minlen=1,
    nullable=False
)


class UpdateUserDetail(BaseCommannd):
    def __init__(self, user_id, data):
        self.user_id = user_id

        if 'birth_day' in data:
            data['birth_day'] = str(datetime.strptime(data['birth_day'], '%Y-%m-%d'))

        self.data = data

    def execute(self):
        session = Session()
        try:
            user = session.query(User).filter_by(id=self.user_id).first()
            if not user:
                session.close()
                raise UserDoesNotExit()

            validate_user_detail_update(self.data)

            if self.email_exist(session, self.data.get('email', None)):
                session.close()
                raise UserAlreadyExists()

            user.name = self.data.get('name', user.name)
            user.email = self.data.get('email', user.email)
            user.birth_day = self.data.get('birth_day', user.birth_day)
            user.city = self.data.get('city', user.city)
            user.phone = self.data.get('phone', user.phone)

            session.commit()

            user = UserJsonSchema().dump(user)
            session.close()

            return user
        except exc.ValidationError as error:
            print(error)
            raise InvalidParams()
        except Exception as error:
            raise error
        finally:
            session.close()

    def email_exist(self, session, email):
        if email is None:
            return False

        return len(session.query(User).filter(User.email == email, User.id != self.user_id).all()) > 0
