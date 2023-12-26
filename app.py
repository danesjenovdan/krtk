from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from routes import init_routes

db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///data.db"
    db.init_app(app)
    migrate.init_app(app, db)

    # Define routes
    init_routes(app)

    return app
