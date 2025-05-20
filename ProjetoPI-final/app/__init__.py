from flask import Flask


def create_app():
    app = Flask(__name__)
    

    # Configurações do banco de dados
    app.config['MYSQL_HOST']     = 'localhost'
    app.config['MYSQL_USER']     = 'root'
    app.config['MYSQL_PASSWORD'] = 'Elisangela@77'
    app.config['MYSQL_DB']       = 'gestao_db'

    with app.app_context():
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp, url_prefix='/')

        from .chat import bp_chat
        app.register_blueprint(bp_chat)

        from .db import init_db, close_db
        init_db()
        app.teardown_appcontext(close_db)

    return app
