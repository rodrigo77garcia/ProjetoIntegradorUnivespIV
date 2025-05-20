import os
import pytest
from dotenv import load_dotenv
from app import create_app

# Carregar variáveis de ambiente do .env
load_dotenv()

# Aplicação Flask global para os testes
@pytest.fixture(scope='module')
def app():
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DEBUG": True,
        "SECRET_KEY": os.getenv("SECRET_KEY")
    })

    with app.app_context():
        yield app

# Client de teste para fazer chamadas HTTP
@pytest.fixture(scope='module')
def client(app):
    return app.test_client()
# Runner de teste para executar comandos de linha de comando