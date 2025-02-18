import csv
from datetime import datetime

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy


def init_commands(app: Flask, db: SQLAlchemy) -> None:
    from db import ShortenedLink

    @click.command("import-csv")
    @click.argument("filepath")
    @with_appcontext
    def import_csv(filepath: str) -> int:
        try:
            with open(filepath, "r") as f:
                reader = csv.reader(f, escapechar="\\")
                count = 0

                click.echo("Importing shortlinks...", nl=False)

                for row in reader:
                    if len(row) != 4:
                        print(row)
                        raise ValueError("Malformed row")

                    alias, destination, created_at_str, clicks = row

                    if created_at_str == "0000-00-00 00:00:00":
                        created = datetime.fromtimestamp(0)
                    else:
                        created = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")

                    shortened_link = ShortenedLink(
                        alias=alias,
                        destination=destination,
                        created=created,
                        is_custom=False,
                    )

                    db.session.add(shortened_link)
                    count += 1

                    if count % 100 == 0:
                        db.session.commit()
                        click.echo(f"\rImported {count} shortlinks", nl=False)

                db.session.commit()
                click.echo(f"\nSuccessfully imported {count} shortlinks")
        except Exception as e:
            click.echo(f"\nError importing data: {str(e)}", err=True)
            db.session.rollback()
            return 1
        return 0

    @click.command("clear-db")
    @click.confirmation_option(
        prompt="Are you sure you want to clear all records from the database?"
    )
    @with_appcontext
    def clear_db() -> int:
        try:
            count = db.session.query(ShortenedLink).delete()
            db.session.commit()
            click.echo(f"Successfully deleted {count} records from the database")
        except Exception as e:
            click.echo(f"Error clearing database: {str(e)}", err=True)
            db.session.rollback()
            return 1
        return 0

    # Register all commands with the app
    app.cli.add_command(import_csv)
    app.cli.add_command(clear_db)
