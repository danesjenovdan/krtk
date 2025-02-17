from typing import cast

from flask import Flask, make_response, redirect, render_template, request
from werkzeug.wrappers.response import Response

from custom_types import ShortenedLinkPayload

DJND_MAIN_PAGE_URL = "https://danesjenovdan.si"
DJND_SHORT_DOMAIN = "djnd.si"


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

    # legacy route for backwards compatibility
    @app.route("/yomamasofat", methods=["GET", "POST"], strict_slashes=False)
    def legacy_shorten_link() -> Response:
        dest = None
        json_data = request.get_json(silent=True)
        if json_data is not None:
            dest = json_data.get("fatmama")
        if not dest:
            dest = request.values.get("fatmama")
        if not dest:
            response = make_response("Enter a URL.", 200)
            response.mimetype = "text/plain"
            return response

        payload_dict = {"destination": dest}
        if errors := validate_shorten_link_payload(payload_dict):
            try:
                error = errors["destination"][0]
            except:
                error = "Unknown error."
            response = make_response(error, 200)
            response.mimetype = "text/plain"
            return response

        payload = cast(ShortenedLinkPayload, payload_dict)
        link = create_shortened_link(payload)
        link_dict = link.to_json()
        short_url = f'https://{DJND_SHORT_DOMAIN}/{link_dict["alias"]}'

        response = make_response(short_url, 200)
        response.mimetype = "text/plain"
        return response

    @app.route("/<alias>")
    def redirect_to_previously_shortened_url(alias: str) -> Response:
        destination = get_destination_for_alias(alias)

        if destination:
            return redirect(destination)
        else:
            return redirect(f"{DJND_MAIN_PAGE_URL}/404")
