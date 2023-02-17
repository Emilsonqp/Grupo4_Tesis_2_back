from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

class SessionConfig():
  def __init__(self):
    print('')

  def url(self):
    db_config = self.config()
    return f'postgresql://admin:W3aEjkV9FBA1ljAFi8zW1y17hJkWLknx@dpg-cfdjkg82i3mmlo2lef1g-a.oregon-postgres.render.com:5432/dermoapp'

  def config(self):
    db_name = os.environ['DB_NAME'] if 'DB_NAME' in os.environ else 'dermoapp'


    base_config = {
      'host': os.environ['DB_HOST'] if 'DB_HOST' in os.environ else 'localhost',
      'port': os.environ['DB_PORT'] if 'DB_PORT' in os.environ else '5432',
      'user': os.environ['DB_USER'] if 'DB_USER' in os.environ else 'postgres',
      'password': os.environ['DB_PASSWORD'] if 'DB_PASSWORD' in os.environ else 'postgres',
      'db': db_name
    }

    return base_config

session_config = SessionConfig()
engine = create_engine(session_config.url())
Session = sessionmaker(bind=engine)