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
  birth_day = Column(DateTime)
  city = Column(String)
  phone = Column(String)
  specialty = Column(String)
  password = Column(String)
  token = Column(String)

  def __init__(self, name, email, birth_day, city, phone,specialty, password):
    Model.__init__(self)
    self.name = name
    self.email = email
    self.birth_day = birth_day
    self.city = city
    self.phone = phone
    self.specialty = specialty

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
  birth_day = fields.DateTime()
  city = fields.Str()
  phone = fields.Str()
  specialty = fields.Str()

class SpecialistJsonSchema(Schema):
  id = fields.Number()
  name = fields.Str()
  email = fields.Str()
  birth_day = fields.DateTime()
  city = fields.Str()
  phone = fields.Str()
  specialty = fields.Str()
  token = fields.Str()
