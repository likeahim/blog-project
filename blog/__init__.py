from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
app = None

def create_app(config_class=Config):
    global app
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Entry": models.Entry
        }

    from blog import routes, models

    return app