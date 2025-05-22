from .extensions import db
from sqlalchemy import Enum
import enum

class Ferramenta(db.Model):
    __tablename__ = 'ferramentas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    local = db.Column(db.String(255))
    descricao = db.Column(db.Text)
    marca = db.Column(db.String(255))
    data_do_emprestimo = db.Column(db.Date)
    data_da_devolucao = db.Column(db.Date)
    nome_funcionario = db.Column(db.String(255))
    setor_de_trabalho = db.Column(db.String(255))
    imagem = db.Column(db.String(255))


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(255))
    endereco = db.Column(db.String(255))

class TipoCliente(enum.Enum):
    Entrada = 'Entrada'
    Saída = 'Saída'

class Financa(db.Model):
    __tablename__ = 'financas'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date)
    descricao = db.Column(db.Text)
    valor = db.Column(db.Numeric(10, 2))
    tipo = db.Column(db.Enum(TipoCliente), nullable=False)


class Organizacao(db.Model):
    __tablename__ = 'organizacao'
    id = db.Column(db.Integer, primary_key=True)
    nome_departamento = db.Column(db.String(255))
    responsavel = db.Column(db.String(255))
    telefone_departamento = db.Column(db.String(15))
