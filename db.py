import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression
from sqlalchemy import Boolean, DateTime, func, Text

from app import db


# The type error on the next line is silenced because mypy can't handle it:
# https://github.com/python/mypy/issues/8603
class ShortenedLink(db.Model):  # type: ignore
    __tablename__ = "shortened_link"

    alias: Mapped[str] = mapped_column(Text, primary_key=True, unique=True)
    destination: Mapped[str] = mapped_column(Text, nullable=False)
    created: Mapped[datetime.date] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    is_custom: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=expression.false()
    )

    def to_json(self) -> dict[str, str]:
        return {"alias": self.alias, "destination": self.destination}


def get_link_count_by_alias(alias: str) -> int:
    # This is apparently how you correctly do a count in SQLAlchemy 2
    # https://github.com/sqlalchemy/sqlalchemy/issues/5908
    statement = (
        db.select(db.func.count()).select_from(ShortenedLink).filter_by(alias=alias)
    )
    existing_link_count: int = db.session.scalar(statement)

    return existing_link_count


def get_link_by_destination(destination: str) -> ShortenedLink | None:
    # This specifically filters out custom links because we don't want to expose
    # someone's manually defined short URL.
    statement = (
        db.select(ShortenedLink)
        .filter_by(destination=destination, is_custom=False)
        .limit(1)
    )
    existing_link: ShortenedLink | None = db.session.scalar(statement)

    return existing_link


def get_link_by_alias(alias: str) -> ShortenedLink | None:
    statement = db.select(ShortenedLink).filter_by(alias=alias).limit(1)
    link: ShortenedLink | None = db.session.scalar(statement)

    return link


def get_latest_non_custom_link() -> ShortenedLink | None:
    statement = (
        db.select(ShortenedLink)
        .filter_by(is_custom=False)
        .order_by(ShortenedLink.created.desc())
        .limit(1)
    )
    link: ShortenedLink | None = db.session.scalar(statement)

    return link


def insert_link(destination: str, alias: str, is_custom: bool) -> ShortenedLink:
    new_link = ShortenedLink(alias=alias, destination=destination, is_custom=is_custom)
    db.session.add(new_link)
    db.session.commit()

    return new_link
