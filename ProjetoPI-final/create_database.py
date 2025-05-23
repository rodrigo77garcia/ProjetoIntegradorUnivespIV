import mysql.connector


def create_database():
    # Conecta ao servidor MySQL
    connection = mysql.connector.connect(
        host="US-PF3LWDPS",
        user="root",
        password="Elisangela@77"
    )

    # Cria um cursor para executar comandos SQL
    cursor = connection.cursor()

    # Verifica se o banco de dados já existe
    cursor.execute("SHOW DATABASES LIKE 'gestao_db'")
    db_exists = cursor.fetchone()

    if db_exists:
        print("O banco de dados 'gestao_db' já existe.")
    else:
        # Comando SQL para criar o banco de dados
        create_database_query = "CREATE DATABASE gestao_db"
        cursor.execute(create_database_query)
        print("Banco de dados 'gestao_db' criado com sucesso.")

    # Fecha o cursor e a conexão
    cursor.close()
    connection.close()


def create_tables():
    # Conecta ao banco de dados 'gestao_db'
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Elisangela@77",
        database="gestao_db"
    )

    # Cria um cursor para executar comandos SQL
    cursor = connection.cursor()

    # Tabela 'ferramentas'
    create_ferramentas_table = """
    CREATE TABLE IF NOT EXISTS ferramentas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(30),
        local VARCHAR(30),
        descricao VARCHAR(50),
        marca VARCHAR(50),
        data_do_emprestimo DATE,
        data_da_devolucao DATE,
        nome_funcionario VARCHAR(30),
        setor_de_trabalho VARCHAR(30),
        imagem VARCHAR(30)
    )
    """
    cursor.execute(create_ferramentas_table)

    # Tabela 'clientes'
    create_clientes_table = """
    CREATE TABLE IF NOT EXISTS clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(50),
        telefone VARCHAR(15),
        email VARCHAR(50),
        endereco VARCHAR(100)
    )
    """
    cursor.execute(create_clientes_table)

    # Tabela 'financas'
    create_financas_table = """
    CREATE TABLE IF NOT EXISTS financas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data DATE,
        descricao VARCHAR(100),
        valor DECIMAL(10, 2),
        tipo ENUM('Entrada', 'Saída')  -- 'Entrada' para receitas e 'Saída' para despesas
    )
    """
    cursor.execute(create_financas_table)

    # Tabela 'organizacao'
    create_organizacao_table = """
    CREATE TABLE organizacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(20),
    endereco VARCHAR(200),
    telefone VARCHAR(20),
    email VARCHAR(100),
    decricao TEXT
    );
    """
    cursor.execute(create_organizacao_table)

    # Confirma as alterações no banco de dados
    connection.commit()
    print("Tabelas criadas com sucesso.")

    # Fecha o cursor e a conexão
    cursor.close()
    connection.close()


# Chama as funções para criar o banco de dados e as tabelas
create_database()
create_tables()

print("Processo de criação de banco de dados e tabelas concluído.")
