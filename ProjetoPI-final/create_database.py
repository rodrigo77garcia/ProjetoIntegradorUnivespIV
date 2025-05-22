import os
import mysql.connector
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()


def create_tables():
    try:
        # Conecta ao banco do Railway
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "mysql.railway.internal"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv(
                "MYSQL_PASSWORD", "AyqLoutFQEZApbsRHappGyihdqOEOoRb"),
            database=os.getenv("MYSQL_DATABASE", "railway")
        )

        cursor = connection.cursor()

        # Cria tabela ferramentas (ajuste conforme necessário)
        create_ferramentas_table = """
        CREATE TABLE IF NOT EXISTS ferramentas (
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
        )
        """
        cursor.execute(create_ferramentas_table)

        # Tabela clientes
        create_clientes_table = """
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255),
            telefone VARCHAR(15),
            email VARCHAR(255),
            endereco VARCHAR(255)
        )
        """
        cursor.execute(create_clientes_table)

        # Tabela financas
        create_financas_table = """
        CREATE TABLE IF NOT EXISTS financas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data DATE,
            descricao TEXT,
            valor DECIMAL(10, 2),
            tipo ENUM('Entrada', 'Saída')
        )
        """
        cursor.execute(create_financas_table)

        # Tabela organizacao
        create_organizacao_table = """
        CREATE TABLE IF NOT EXISTS organizacao (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome_departamento VARCHAR(255),
            responsavel VARCHAR(255),
            telefone_departamento VARCHAR(15)
        )
        """
        cursor.execute(create_organizacao_table)

        print("Tabelas criadas com sucesso.")

    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
