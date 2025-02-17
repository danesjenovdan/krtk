from typing import Any

from marshmallow import Schema, ValidationError, fields, validate

from routes import DJND_SHORT_DOMAIN
from services import link_with_alias_exists


def _validate_unique_alias(alias: str) -> None:
    if link_with_alias_exists(alias):
        raise ValidationError(f"Alias `{alias}` already in use.", "alias")


def _validate_not_short_url(destination: str) -> None:
    if destination.startswith(
        (f"https://{DJND_SHORT_DOMAIN}", f"http://{DJND_SHORT_DOMAIN}")
    ):
        raise ValidationError("Already a short URL.", "destination")


class ShortenLinkPayloadSchema(Schema):
    destination = fields.Url(required=True)
    alias = fields.String(validate=[validate.Regexp("^[a-zA-Z0-9_-]*$")])


def validate_shorten_link_payload(payload: Any) -> dict[str, list[str]] | None:
    schema = ShortenLinkPayloadSchema()

    try:
        schema.load(payload)
        if alias := payload.get("alias"):
            _validate_unique_alias(alias)
        _validate_not_short_url(payload["destination"])
        return None
    except ValidationError as err:
        error_messages = err.normalized_messages()  # type: ignore[no-untyped-call]
        assert isinstance(error_messages, dict)
        return error_messages
