"""Initialize app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    '''Construct the flask core app object.'''

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('src.config.Config')

    # Initialize plugins.
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        import src.routes as routes
        import src.login.routes as login

        # Register routes.
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(login.auth_bp)

        db.create_all()

        return app
