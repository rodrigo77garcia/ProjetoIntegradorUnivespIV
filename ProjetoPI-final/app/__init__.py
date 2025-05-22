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
    migrate.init_app(app, db)

    # Executa migrações na primeira requisição
    @app.before_first_request
    def apply_migrations():
        try:
            print("Aplicando migrações automaticamente...")
            from flask_migrate import upgrade, migrate as run_migrate

            # Ativa o contexto da app
            with app.app_context():
                # Rode o equivalente a `flask db migrate` e `flask db upgrade`
                run_migrate(message="Auto migration on first request")
                upgrade()
                print("Migrações aplicadas com sucesso!")
        except Exception as e:
            print(f"Erro ao aplicar migrações: {e}")

    # Registro dos blueprints
    with app.app_context():
        from .models import Ferramenta, Cliente, Financa, Organizacao

        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp, url_prefix='/')

        from .chat import bp_chat
        app.register_blueprint(bp_chat)

    return app