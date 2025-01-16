from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import URL
import os
from routes import init_routes

db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(
        "postgresql+psycopg",
        host=os.getenv("FLASK_DATABASE_HOST", "db"),
        database=os.getenv("FLASK_DATABASE_NAME", "flask"),
        username=os.getenv("FLASK_DATABASE_USERNAME", "flask"),
        password=os.getenv("FLASK_DATABASE_PASSWORD", "changeme"),
        port=os.getenv("FLASK_DATABASE_PORT", "5432"),
    )
    db.init_app(app)
    migrate.init_app(app, db)

    # Define routes
    init_routes(app)

    return app
