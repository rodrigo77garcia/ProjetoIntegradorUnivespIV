from flask import Flask
from .extensions import db, migrate
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def create_app():
    # Carregar variáveis do .env
    load_dotenv()

    app = Flask(__name__)

    # Configurações do banco de dados
    db_uri = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    print("DEBUG: DATABASE_URL =", db_uri)  # <-- Linha adicionada
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa a extensão SQLAlchemy
    db.init_app(app)
    # Inicializa a extensão Migrate
    migrate.init_app(app, db)

    # Registro dos blueprints
    with app.app_context():
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp, url_prefix='/')

        from .chat import bp_chat
        app.register_blueprint(bp_chat)

    return app
