from app import create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = create_app()

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql -h gondola.proxy.rlwy.net -u root -p AyqLoutFQEZApbsRHappGyihdqOEOoRb --port 26546 --protocol=TCP railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.config['DEBUG']=True
    app.run(debug=True)
