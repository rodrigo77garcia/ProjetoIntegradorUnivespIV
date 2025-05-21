# utilizando o Flask
from flask import Blueprint, request, jsonify, render_template, current_app, url_for, redirect, flash
from .db import get_db
from datetime import datetime
import logging
from flask import flash
import os
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = Blueprint('routes', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


###########################################################
# CRUD Ferramentas
###########################################################

UPLOAD_FOLDER = 'static/uploads'  # caminho onde salvará as imagens
# extensões permitidas para upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# Verifica se a extensão do arquivo é permitida
#


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota para adicionar uma ferramenta


@bp.route('/add', methods=['POST'])
def add_ferramenta():
    nome = request.form.get('nome')
    local = request.form.get('local')
    descricao = request.form.get('descricao')
    marca = request.form.get('marca')
    data_do_emprestimo_str = request.form.get('data_do_emprestimo')
    data_da_devolucao_str = request.form.get('data_da_devolucao')
    nome_funcionario = request.form.get('nome_funcionario')
    setor_de_trabalho = request.form.get('setor_de_trabalho')
    imagem_file = request.files.get('imagem')

    # Debug: Print values to check if they are correctly received
    print(f"Received: nome={nome}, local={local}, descricao={descricao}, marca={marca}, data_do_emprestimo={data_do_emprestimo_str}, data_da_devolucao={data_da_devolucao_str}, nome_funcionario={nome_funcionario}, setor_de_trabalho={setor_de_trabalho}, imagem={imagem}")

    data_do_emprestimo = datetime.strptime(
        data_do_emprestimo_str, '%Y-%m-%d') if data_do_emprestimo_str else None
    data_da_devolucao = datetime.strptime(
        data_da_devolucao_str, '%Y-%m-%d') if data_da_devolucao_str else None

    imagem_path = None
    if imagem_file and allowed_file(imagem_file.filename):
        filename = secure_filename(imagem_file.filename)
        # Cria o diretório se não existir
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        full_path = os.path.join(UPLOAD_FOLDER, filename)
        imagem_file.save(full_path)
        imagem_path = full_path

    db = get_db()
    cursor = db.cursor()

    query = """
    INSERT INTO ferramentas (nome, local, descricao, marca, data_do_emprestimo, data_da_devolucao, nome_funcionario, setor_de_trabalho, imagem)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (nome, local, descricao, marca, data_do_emprestimo,
                       data_da_devolucao, nome_funcionario, setor_de_trabalho, imagem_path))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return jsonify({"message": "Erro ao adicionar a ferramenta", "error": str(e)}), 500
    finally:
        cursor.close()

    return jsonify({"message": "Ferramenta adicionada com sucesso"}), 201

# Rota para atualizar uma ferramenta existente


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update_ferramenta(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM ferramentas WHERE id = %s', (id,))
    ferramenta = cursor.fetchone()

    if ferramenta is None:
        # Caso o ID não exista, redirecionar para a lista de ferramentas com uma mensagem de erro
        cursor.close()
        return redirect(url_for('routes.listar_ferramentas'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        local = request.form.get('local')
        descricao = request.form.get('descricao')
        marca = request.form.get('marca')
        data_do_emprestimo_str = request.form.get('data_do_emprestimo')
        data_da_devolucao_str = request.form.get('data_da_devolucao')
        nome_funcionario = request.form.get('nome_funcionario')
        setor_de_trabalho = request.form.get('setor_de_trabalho')
        imagem = request.form.get('imagem')

        data_do_emprestimo = datetime.strptime(
            data_do_emprestimo_str, '%Y-%m-%d') if data_do_emprestimo_str else None
        data_da_devolucao = datetime.strptime(
            data_da_devolucao_str, '%Y-%m-%d') if data_da_devolucao_str else None

        query = """
        UPDATE ferramentas
        SET nome = %s, local = %s, descricao = %s, marca = %s, data_do_emprestimo = %s, data_da_devolucao = %s, nome_funcionario = %s, setor_de_trabalho = %s, imagem = %s
        WHERE id = %s
        """
        cursor.execute(query, (nome, local, descricao, marca, data_do_emprestimo,
                       data_da_devolucao, nome_funcionario, setor_de_trabalho, imagem, id))
        db.commit()
        cursor.close()
        return redirect(url_for('routes.listar_ferramentas'))

    return render_template('update_ferramenta.html', ferramenta=ferramenta)

# Rota para deletar uma ferramenta


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_ferramenta(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ferramentas WHERE id = %s", (id,))
    ferramenta = cursor.fetchone()

    if ferramenta is None:
        # Caso o ID não exista, redirecionar para a lista de ferramentas com uma mensagem de erro
        cursor.close()
        return redirect(url_for('routes.listar_ferramentas'))

    if request.method == 'POST':
        cursor.execute("DELETE FROM ferramentas WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        return redirect(url_for('routes.listar_ferramentas'))

    cursor.close()
    return render_template('delete_ferramenta.html', ferramenta=ferramenta)

# Rota para listar todas as ferramentas


@bp.route('/ferramentas/listar', methods=['GET'])
def listar_ferramentas():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ferramentas")
    ferramentas = cursor.fetchall()
    cursor.close()
    print(ferramentas)  # Linha para depurar

    return render_template('listar_ferramentas.html', ferramentas=ferramentas)

# Rota para listar uma ferramenta individualmente


@bp.route('/ferramentas/<int:id>', methods=['GET'])
def listar_ferramentasID(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ferramentas WHERE id = %s", (id,))
    ferramenta = cursor.fetchone()
    cursor.close()
    if ferramenta:
        return jsonify(ferramenta)
    else:
        return jsonify({"message": "Ferramenta não encontrada"}), 404

############################################################
# CRUD Clientes
############################################################

# Rota para adicionar um cliente


@bp.route('/add_cliente', methods=['POST'])
def add_cliente():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')

    db = get_db()
    cursor = db.cursor()

    query = """
    INSERT INTO clientes (nome, email, telefone, endereco)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (nome, email, telefone, endereco))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return jsonify({"message": "Erro ao adicionar o cliente", "error": str(e)}), 500
    finally:
        cursor.close()

    return jsonify({"message": "Cliente adicionado com sucesso"}), 201

# Rota para listar todos os clientes


@bp.route('/clientes/listar', methods=['GET'])
def listar_clientes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()

    return render_template('listar_clientes.html', clientes=clientes)

# Rota para atualizar um cliente existente


@bp.route('/update_cliente/<int:id>', methods=['GET', 'POST'])
def update_cliente(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id = %s', (id,))
    cliente = cursor.fetchone()

    if cliente is None:
        cursor.close()
        return redirect(url_for('routes.listar_clientes'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')

        query = """
        UPDATE clientes
        SET nome = %s, email = %s, telefone = %s, endereco = %s
        WHERE id = %s
        """
        cursor.execute(query, (nome, email, telefone, endereco, id))
        db.commit()
        cursor.close()
        return redirect(url_for('routes.listar_clientes'))

    return render_template('atualizar_cliente.html', cliente=cliente)

# Rota para deletar um cliente


@bp.route('/delete_cliente/<int:id>', methods=['GET', 'POST'])
def delete_cliente(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()

    if cliente is None:
        cursor.close()
        return redirect(url_for('routes.listar_clientes'))

    if request.method == 'POST':
        cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        return redirect(url_for('routes.listar_clientes'))

    cursor.close()
    return render_template('delete_cliente.html', cliente=cliente)

# Rota para listar um cliente individualmente


@bp.route('/clientes/<int:id>', methods=['GET'])
def listar_clientesID(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    if cliente:
        return jsonify(cliente)
    else:
        return jsonify({"message": "Cliente não encontrado"}), 404

############################################################
# CRUD Finanças
############################################################

# Rota para adicionar um registro financeiro


def get_financas():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM financas")
    financas = cursor.fetchall()
    cursor.close()
    return financas


@bp.route('/add_financas', methods=['GET', 'POST'])
def add_financas():
    mensagem = None
    tipo = None

    if request.method == 'POST':
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        data_str = request.form.get('data')

        data = datetime.strptime(data_str, '%Y-%m-%d') if data_str else None

        db = get_db()
        cursor = db.cursor()

        query = """
        INSERT INTO financas (descricao, valor, data)
        VALUES (%s, %s, %s)
        """
        try:
            cursor.execute(query, (descricao, valor, data))
            db.commit()
            mensagem = "Registro financeiro adicionado com sucesso"
            tipo = "success"
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
            mensagem = "Erro ao adicionar o registro financeiro"
            tipo = "error"
        finally:
            cursor.close()

        financas = get_financas()

        return render_template('listar_financas.html', financas=financas, mensagem=mensagem, tipo=tipo)

    return render_template('adicionar_financa.html')

# Rota para listar todos os registros financeiros


@bp.route('/listar_financas', methods=['GET'])
def listar_financas():
    financas = get_financas()

    if request.headers.get("Accept") == "application/json":
        return jsonify(financas)

    return render_template('listar_financas.html', financas=financas)

# Rota para atualizar um registro financeiro existente


@bp.route('/update_financa/<int:id>', methods=['GET', 'POST'])
def update_financa(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM financas WHERE id = %s', (id,))
    financa = cursor.fetchone()

    if not financa:
        cursor.close()
        financas = get_financas()
        return render_template('listar_financas.html', financas=financas, mensagem="Registro financeiro não encontrado", tipo="error")

    if request.method == 'POST':
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        data_str = request.form.get('data')

        data = datetime.strptime(data_str, '%Y-%m-%d') if data_str else None

        query = """
        UPDATE financas
        SET descricao = %s, valor = %s, data = %s
        WHERE id = %s
        """
        try:
            cursor.execute(query, (descricao, valor, data, id))
            db.commit()
            mensagem = "Registro financeiro atualizado com sucesso"
            tipo = "success"
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
            mensagem = f'Erro ao atualizar o registro financeiro: {e}'
            tipo = "error"
        finally:
            cursor.close()

        financas = get_financas()
        return render_template('listar_financas.html', financas=financas, mensagem=mensagem, tipo=tipo)
    # Se não for um POST, apenas renderiza o formulário de atualização

    return render_template('atualizar_financa.html', financa=financa)

# Rota para deletar um registro financeiro


@bp.route('/delete_financa/<int:id>', methods=['GET', 'POST'])
def delete_financa(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM financas WHERE id = %s", (id,))
    financa = cursor.fetchone()

    if not financa:
        cursor.close()
        financas = get_financas()
        return render_template('listar_financas.html', financas=financas, mensagem="Registro financeiro não encontrado", tipo="error")
    # Se o registro não for encontrado, redireciona para a lista de finanças

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM financas WHERE id = %s", (id,))
            db.commit()
            mensagem = "Registro financeiro deletado com sucesso"
            tipo = "success"
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
            mensagem = f'Erro ao deletar o registro financeiro: {e}'
            tipo = "error"
        finally:
            cursor.close()

        financas = get_financas()
        return render_template('listar_financas.html', financas=financas, mensagem=mensagem, tipo=tipo)

    cursor.close()
    return render_template('delete_financa.html', financa=financa)

# Rota para listar um registro financeiro individualmente (API JSON)


@bp.route('/financas/<int:id>', methods=['GET'])
def listar_financa_por_id(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM financas WHERE id = %s", (id,))
    financa = cursor.fetchone()
    cursor.close()

    if financa:
        return jsonify(financa)
    else:
        return jsonify({"message": "Registro financeiro não encontrado"}), 404

# Conectar e desconectar ao banco de dados automaticamente


@bp.before_app_request
def before_request():
    db = get_db()
    if not hasattr(current_app, 'db'):
        current_app.db = db


@bp.teardown_app_request
def teardown_request(exception):
    if hasattr(current_app, 'db'):
        current_app.db.close()


############################################################
# CRUD Organização
############################################################

# Rota para adicionar um recurso de organização
@bp.route('/add_organizacao', methods=['GET', 'POST'])
def add_organizacao():
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        data_str = request.form.get('data')

        data = datetime.strptime(data_str, '%Y-%m-%d') if data_str else None

        db = get_db()
        cursor = db.cursor()

        query = """
        INSERT INTO organizacao (descricao, valor, data)
        VALUES (%s, %s, %s)
        """
        try:
            cursor.execute(query, (descricao, valor, data))
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
            return jsonify({"message": "Erro ao adicionar o recurso de organização", "error": str(e)}), 500
        finally:
            cursor.close()

        return redirect(url_for('routes.listar_organizacao'))

    return render_template('adicionar_organizacao.html')

# Rota para listar todos os registros de organização


@bp.route('/organizacao/listar', methods=['GET'])
def listar_organizacao():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM organizacao")
    organizacao = cursor.fetchall()
    cursor.close()

    return render_template('listar_organizacao.html', organizacao=organizacao)

# Rota para atualizar um registro de organização existente


@bp.route('/update_organizacao/<int:id>', methods=['GET', 'POST'])
def update_organizacao(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM organizacao WHERE id = %s', (id,))
    organizacao = cursor.fetchone()

    if not organizacao:
        cursor.close()
        return redirect(url_for('routes.listar_organizacao'))

    if request.method == 'POST':
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        data_str = request.form.get('data')

        data = datetime.strptime(data_str, '%Y-%m-%d') if data_str else None

        query = """
        UPDATE organizacao
        SET descricao = %s, valor = %s, data = %s
        WHERE id = %s
        """
        cursor.execute(query, (descricao, valor, data, id))
        db.commit()
        cursor.close()
        return redirect(url_for('routes.listar_organizacao'))

    return render_template('atualizar_organizacao.html', organizacao=organizacao)

# Rota para deletar um registro de organização


@bp.route('/delete_organizacao/<int:id>', methods=['GET', 'POST'])
def delete_organizacao(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM organizacao WHERE id = %s", (id,))
    organizacao = cursor.fetchone()

    if not organizacao:
        cursor.close()
        return redirect(url_for('routes.listar_organizacao'))

    if request.method == 'POST':
        cursor.execute("DELETE FROM organizacao WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        return redirect(url_for('routes.listar_organizacao'))

    cursor.close()
    return render_template('delete_organizacao.html', organizacao=organizacao)

# Rota para listar um registro de organização individualmente (API JSON)


@bp.route('/organizacao/<int:id>', methods=['GET'])
def listar_organizacao_por_id(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM organizacao WHERE id = %s", (id,))
    organizacao = cursor.fetchone()
    cursor.close()

    if organizacao:
        return jsonify(organizacao)
    else:
        return jsonify({"message": "Registro de organização não encontrado"}), 404

################################################################
# Páginas Web
################################################################

# Rota para a página de ferramentas


@bp.route('/ferramentas', methods=['GET'])
def ferramentas():
    return render_template('index_ferramentas.html')

# Rota para a página de finanças


@bp.route('/financas', methods=['GET'])
def financas():
    return render_template('index_financas.html')

# Rota para a página de clientes


@bp.route('/clientes', methods=['GET'])
def clientes():
    return render_template('index_clientes.html')

# Rota para a página de organização


@bp.route('/organizacao', methods=['GET'])
def organizacao():
    return render_template('index_organizacao.html')
