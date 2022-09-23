from flask import Flask
from os import environ
from dotenv import load_dotenv

load_dotenv()

def init_app(app: Flask):
    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')