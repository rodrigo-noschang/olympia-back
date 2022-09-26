from flask import Flask
from flask_migrate import Migrate

def init_app(app: Flask):
    from app.model import user_model
    from app.model import food_model

    Migrate(app, app.db)