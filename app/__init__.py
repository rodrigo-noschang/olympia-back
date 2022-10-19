from venv import create
from flask import Flask
from app.configs import env_configs, database, migrations
from app import routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    env_configs.init_app(app)
    database.init_app(app)
    migrations.init_app(app)
    routes.init_app(app)

    return app

deploy_app = create_app()