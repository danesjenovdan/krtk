import datetime
from typing import Set
from db import ShortenedLink

shortened_links: Set[ShortenedLink] = set()


def clear() -> None:
    shortened_links = set()


def count() -> None:
    return len(shortened_links)


def get_link_count_by_alias(alias: str) -> int:
    links_with_matching_alias = [
        link for link in shortened_links if link.alias == alias
    ]
    return len(links_with_matching_alias)


def get_link_by_destination(destination: str) -> ShortenedLink | None:
    for link in shortened_links:
        if link.destination == destination:
            return link


def get_link_by_alias(alias: str) -> ShortenedLink | None:
    for link in shortened_links:
        if link.alias == alias:
            return link


def get_latest_non_custom_link() -> ShortenedLink | None:
    non_custom_links = [link for link in shortened_links if not link.is_custom]
    sorted_links = sorted(non_custom_links, key=lambda link: link.created)

    return sorted_links[-1] if sorted_links else None


def insert_link(destination: str, alias: str, is_custom: bool) -> ShortenedLink:
    new_link = ShortenedLink(
        alias=alias,
        destination=destination,
        is_custom=is_custom,
        created=datetime.datetime.now(),
    )
    shortened_links.add(new_link)
    return new_link
