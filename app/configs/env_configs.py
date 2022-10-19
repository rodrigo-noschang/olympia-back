from flask import Flask
from os import environ
from dotenv import load_dotenv

load_dotenv()

def init_app(app: Flask):
    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DATABASE_URL'] = environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')