import mysql.connector
from flask import current_app, g
from sqlalchemy.engine.url import make_url
import os


def init_db():
    """Cria o banco e as tabelas se não existirem."""
    try:
        # Extrai a DATABASE_URL do ambiente ou Flask config
        db_url = current_app.config.get('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')
        if not db_url:
            raise ValueError("DATABASE_URL não está definida.")

        url = make_url(db_url)

        db = mysql.connector.connect(
            host=url.host,
            port=url.port or 3306,
            user=url.username,
            password=url.password,
            database=url.database
        )
        cursor = db.cursor()

        # Criar tabela 'ferramentas'
        cursor.execute('''CREATE TABLE IF NOT EXISTS ferramentas (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nome VARCHAR(255),
                            local VARCHAR(255),
                            descricao TEXT,
                            marca VARCHAR(255),
                            data_do_emprestimo DATE,
                            data_da_devolucao DATE,
                            nome_funcionario VARCHAR(255),
                            setor_de_trabalho VARCHAR(255),
                            imagem VARCHAR(255)
                        )''')

        # Tabela clientes
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nome VARCHAR(255),
                            telefone VARCHAR(15),
                            email VARCHAR(255),
                            endereco VARCHAR(255)
                        )''')

        # Tabela finanças
        cursor.execute('''CREATE TABLE IF NOT EXISTS financas (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            data DATE,
                            descricao TEXT,
                            valor DECIMAL(10, 2),
                            tipo ENUM('Entrada', 'Saída')
                        )''')

        # Tabela organizacao
        cursor.execute('''CREATE TABLE IF NOT EXISTS organizacao (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nome_departamento VARCHAR(255),
                            responsavel VARCHAR(255),
                            telefone_departamento VARCHAR(15)
                        )''')

        db.commit()
        cursor.close()
        db.close()
        print("Banco de dados e tabelas criados com sucesso.")
    except Exception as err:
        print(f"Erro ao criar banco de dados: {err}")


def get_db():
    """Retorna uma conexão reutilizável com o banco."""
    if 'db' not in g:
        db_url = current_app.config.get('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')
        if not db_url:
            raise ValueError("DATABASE_URL não está definida.")

        url = make_url(db_url)

        g.db = mysql.connector.connect(
            host=url.host,
            port=url.port or 3306,
            user=url.username,
            password=url.password,
            database=url.database
        )
    return g.db


def close_db(e=None):
    """Fecha a conexão com o banco ao final da requisição."""
    db = g.pop('db', None)
    if db is not None:
        db.close()