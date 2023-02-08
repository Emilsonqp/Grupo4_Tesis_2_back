from marshmallow import  Schema, fields
from sqlalchemy import Column, String, DateTime
from .model import Model, Base
from datetime import datetime, timedelta
from uuid import uuid4
import argon2

class Specialist(Model, Base):
  __tablename__ = 'specialist'

  name = Column(String)
  email = Column(String)
  last_name = Column(String)
  username = Column(String)
  password = Column(String)
  token = Column(String)

  def __init__(self, name, email, last_name, username, password):
    Model.__init__(self)
    self.name = name
    self.email = email
    self.last_name = last_name
    self.username = username

    ph = argon2.PasswordHasher()
    self.password = ph.hash(password.encode('utf-8'))
    self.set_token()

  def set_token(self):
    self.token = uuid4()

class SpecialistSchema(Schema):
  id = fields.Number()
  name = fields.Str()
  email = fields.Str()
  password = fields.Str()
  last_name = fields.Str()
  username = fields.Str()

class SpecialistJsonSchema(Schema):
  id = fields.Number()
  name = fields.Str()
  email = fields.Str()
  password = fields.Str()
  last_name = fields.Str()
  username = fields.Str()
  token = fields.Str()
