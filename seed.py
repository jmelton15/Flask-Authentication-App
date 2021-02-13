""" Seed file for creating the tables in our database """

from models import db
from app import app

db.drop_all()
db.create_all()