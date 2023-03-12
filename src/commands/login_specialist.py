from .base_command import BaseCommannd
from ..models.specialist import Specialist
from ..session import Session
from flask import request
from flask_jwt_extended import create_access_token
from ..errors.errors import InvalidParams, SpecialistIsNotRegister, SpecialistWrongPassword
import argon2


class LoginSpecialist(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        session = Session()
        ph = argon2.PasswordHasher()
        try:
            if 'email' not in self.data or 'password' not in self.data:
                raise InvalidParams()
            
            u_username = self.data['email']
            u_password = self.data['password']
            user = session.query(Specialist).filter_by(email=u_username).first()

            if user is None:
                raise SpecialistIsNotRegister()

            pass_hash = user.password
            ph.verify(pass_hash, u_password.encode('utf-8'))
            if ph.check_needs_rehash(pass_hash):
                user.password = ph.hash(u_password.encode('utf-8'))
                session.add(user)
                session.commit()

            access_token = create_access_token(identity=user.email)
            user.token = access_token
            session.add(user)
            session.commit()

            return {"message": "Access granted", "username": {"username": user.username, "id": user.id, "name": user.name, "last_name": user.last_name}, 
                "access_token": access_token}

        except TypeError:
            raise InvalidParams()
        except (argon2.exceptions.VerifyMismatchError, argon2.exceptions.VerificationError, argon2.exceptions.InvalidHash):
            raise SpecialistWrongPassword()
        except Exception as error:
            session.close()
            raise error