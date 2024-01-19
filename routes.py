from typing import cast
from flask import Flask, render_template, redirect, request, make_response
from werkzeug.wrappers.response import Response

from custom_types import ShortenedLinkPayload

DJND_MAIN_PAGE_URL = "https://danesjenovdan.si/"


def init_routes(app: Flask) -> None:
    from services import create_shortened_link, get_destination_for_alias
    from validation import validate_shorten_link_payload

    @app.route("/")
    def redirect_to_main_page() -> Response:
        return redirect(DJND_MAIN_PAGE_URL)

    @app.route("/short")
    def render_index() -> str:
        return render_template("shortener.html")

    @app.route("/_shorten_link", methods=["POST"])
    def shorten_link() -> Response:
        if errors := validate_shorten_link_payload(request.json):
            return make_response(errors, 400)

        payload = cast(ShortenedLinkPayload, request.json)
        link = create_shortened_link(payload)

        return make_response(link.to_json(), 201)

    @app.route("/<alias>")
    def redirect_to_previously_shortened_url(alias: str) -> Response:
        destination = get_destination_for_alias(alias)

        if destination:
            return redirect(destination)
        else:
            return redirect(f"{DJND_MAIN_PAGE_URL}/404")
