# krtk

Basic URL shortener written in Python. Dependencies:
- [Flask](https://flask.palletsprojects.com/) as the framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM
  - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com) for better integration with Flask
  - [Flask-Migrate](https://flask-migrate.readthedocs.io) to handle migrations with Alembic
- [Marshmallow](https://marshmallow.readthedocs.io) for a tiny bit of validation
- [Black](https://black.readthedocs.io) for formatting
- [mypy](https://mypy-lang.org/) for static type checking

The word itself is a vowel-less version of _kratek_, meaning _short_ in
Slovenian. Also sounds like [krtek](https://sl.wikipedia.org/wiki/Krtek) which
seemed cute.

## Dev environment
Things are handled with `pipenv`:

```bash
# Install dependencies
pipenv install -d

# Go into the virtualenv
pipenv shell

# Start the app
flask run --debug


# Run type checker
pipenv run check-types

# Run formatter
pipenv run format

# Run tests
pipenv run test
```

## Migrations
Database migrations use `alembic` through `Flask-Migrate`, refer to the
[official documentation](https://flask-migrate.readthedocs.io/).

Two everyday things you might need:
```bash
# Run any outstanding migrations (needed before first run)
flask db upgrade

# Generate new migration after modifying model in db.py
flask db migrate -m "Add field X to table Y"
```
