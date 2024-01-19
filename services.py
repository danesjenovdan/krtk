import re

import db
from custom_types import ShortenedLinkPayload


def create_shortened_link(payload: ShortenedLinkPayload) -> db.ShortenedLink:
    destination: str = payload["destination"]
    alias: str | None = payload.get("alias")
    is_custom = bool(alias)

    if not is_custom:
        # If the alias isn't a custom one, see if this exact URL was previously
        # shortened and just return that one.
        existing_link = db.get_link_by_destination(destination)
        if existing_link:
            return existing_link

    new_alias = alias

    if not new_alias:
        if last_shortened_link := db.get_latest_non_custom_link():
            last_alias = last_shortened_link.alias
            new_alias = _generate_next_alias(last_alias)
        else:
            # First alias ever 🎉
            new_alias = "a"

    return db.insert_link(destination, new_alias, is_custom)


def get_destination_for_alias(alias: str) -> str | None:
    link = db.get_link_by_alias(alias)
    return link.destination if link else None


def link_with_alias_exists(alias: str) -> bool:
    existing_link_count = db.get_link_count_by_alias(alias)
    return bool(existing_link_count > 0)


def _generate_next_alias(last_alias: str) -> str:
    def get_next_letter(current_letter: str) -> str:
        if current_letter == "z":
            return "a"
        return chr(ord(current_letter) + 1)

    new_alias_list = list(last_alias)

    # Special case: if current string is all "z"s, return a string of all "a"s,
    # but longer by one. E.g. "zzz" -> "aaaa"
    all_zs_regex = re.compile("^z*$")
    if all_zs_regex.match(last_alias):
        return "a" * (len(new_alias_list) + 1)

    # Loop through the string backwards
    for i in range(len(new_alias_list) - 1, -1, -1):
        # Get current letter
        current_letter = new_alias_list[i]

        # Determine next letter in order
        next_letter = get_next_letter(current_letter)

        # Replace current letter with next one in order
        new_alias_list[i] = next_letter

        # If we didn't change a "z" to an "a", we can stop looping. Otherwise
        # continue as the next letter needs to be increased too.
        if next_letter != "a":
            break

    new_alias = "".join(new_alias_list)

    return new_alias
