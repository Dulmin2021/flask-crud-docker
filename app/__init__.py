from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://user:pass@db:5432/itemsdb"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Override with test config if provided (e.g. SQLite in-memory for tests)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import items_bp
    app.register_blueprint(items_bp)

    return app
