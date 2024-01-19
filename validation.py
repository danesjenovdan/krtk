from marshmallow import Schema, fields, ValidationError, validate
from typing import Any

from db import link_with_alias_exists


def _validate_unique_alias(alias: str) -> None:
    if link_with_alias_exists(alias):
        raise ValidationError(f"Alias `{alias}` already in use")


class ShortenLinkPayloadSchema(Schema):
    destination = fields.Url(required=True)
    alias = fields.String(validate=[validate.Regexp("^[a-zA-Z0-9_-]*$")])


def validate_shorten_link_payload(payload: Any) -> dict[str, list[str]] | None:
    schema = ShortenLinkPayloadSchema()

    try:
        schema.load(payload)
        if alias := payload.get("alias"):
            _validate_unique_alias(alias)
        return None
    except ValidationError as err:
        assert isinstance(err.messages, dict)
        return err.messages
