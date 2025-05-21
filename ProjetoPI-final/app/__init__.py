from flask import Flask
from .extensions import db
from dotenv import load_dotenv
import os

def create_app():
    # Carregar variáveis do .env
    load_dotenv()

    app = Flask(__name__)

    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa a extensão SQLAlchemy
    db.init_app(app)

    # Registro dos blueprints
    with app.app_context():
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp, url_prefix='/')

        from .chat import bp_chat
        app.register_blueprint(bp_chat)

    return app
