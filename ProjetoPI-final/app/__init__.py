from flask import Flask
from .extensions import db, migrate
from dotenv import load_dotenv
import os
from sqlalchemy import inspect


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
    # Se você não usa Flask-Migrate, pode remover esta linha
    migrate.init_app(app, db)

    with app.app_context():
        from .models import Ferramenta, Cliente, Financa, Organizacao

        # Lista com os nomes das tabelas existentes
        tabelas_esperadas = ['ferramentas',
                             'clientes', 'financas', 'organizacao']
        inspector = inspect(db.engine)
        tabelas_existentes = inspector.get_table_names()

        # Verifica se todas as tabelas esperadas existem
        todas_tabelas_existentes = all(
            table in tabelas_existentes for table in tabelas_esperadas)

        # Cria todas as tabelas, se ainda não existirem
        try:
            if not todas_tabelas_existentes:
                print("Criando tabelas...")
                db.create_all()
                print("Tabelas criadas com sucesso.")
            else:
                print("Tabelas encontradas. Aplicando migrações, se necessário.")
                from flask_migrate import upgrade
                upgrade()
                print("Migrações aplicadas com sucesso.")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")

        # Registre seus blueprints aqui 👇
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp, url_prefix='/')

        from .chat import bp_chat
        app.register_blueprint(bp_chat)

    return app
