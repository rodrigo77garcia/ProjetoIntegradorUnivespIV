from flask import Flask
from .extensions import db, migrate
from dotenv import load_dotenv
import os

def create_app():
    # Carregar variáveis do .env
    load_dotenv()

    app = Flask(__name__)

    # Configurações do banco de dados
    db_uri = os.getenv('DATABASE_URL')
    if not db_uri:
        raise ValueError("DATABASE_URL não está definida.")

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)  # Se você não usa Flask-Migrate, pode remover esta linha

    with app.app_context():
        # Importe seus modelos aqui 👇
        from .models import Ferramenta, Cliente, Financa, Organizacao

        # Cria todas as tabelas, se ainda não existirem
        try:
            db.create_all()
            print("Tabelas criadas com sucesso (ou já existiam)")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")

        # Registre seus blueprints aqui 👇
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp, url_prefix='/')

        from .chat import bp_chat
        app.register_blueprint(bp_chat)

    return app