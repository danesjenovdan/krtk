from typing import TypedDict


class ShortenedLinkPayload(TypedDict):
    destination: str
    alias: str | None
