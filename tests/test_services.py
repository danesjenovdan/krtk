from tests import mock_db

from unittest import TestCase
from unittest.mock import patch
from services import (
    link_with_alias_exists,
    create_shortened_link,
    get_destination_for_alias,
    _generate_next_alias,
)


@patch("services.db", new=mock_db)
class TestPublicServices(TestCase):
    def setUp(self):
        mock_db.clear()

    def test_create_shortened_link(self):
        first_link = create_shortened_link({"destination": "http://www.example.com"})
        second_link = create_shortened_link(
            {"destination": "http://www.different-example.com"}
        )
        third_link = create_shortened_link({"destination": "http://www.example.com"})
        fourth_link = create_shortened_link(
            {"destination": "http://www.example.com", "alias": "custom-alias"}
        )

        # First two aliases are assigned sequentially.
        self.assertEqual(first_link.alias, "a")
        self.assertEqual(second_link.alias, "b")

        # Third link has the same destination as first link, so we get an
        # existing alias back.
        self.assertEqual(third_link.alias, "a")

        # Fourth link also has the same destination as first link, but because
        # we provided a custom alias, we won't reuse an old one.
        self.assertEqual(fourth_link.alias, "custom-alias")

        # 4 generated links - 1 reused alias = 3 items in DB
        self.assertEqual(mock_db.count(), 3)

    def test_get_destination_for_alias(self):
        mock_db.insert_link("http://www.zombo.com", "zz", False)
        mock_db.insert_link("http://www.example.com", "custom-alias", True)

        self.assertEqual(get_destination_for_alias("zz"), "http://www.zombo.com")
        self.assertEqual(
            get_destination_for_alias("custom-alias"), "http://www.example.com"
        )

        self.assertEqual(get_destination_for_alias("ZZ"), None)
        self.assertEqual(get_destination_for_alias("doesnt-exist"), None)

    def test_link_with_alias_exists(self):
        mock_db.insert_link("http://www.example.com", "a", False)
        mock_db.insert_link("http://www.example.com/foo", "b", False)
        mock_db.insert_link("http://www.example.com", "custom-alias", True)

        # These should exist because we inserted them above
        self.assertTrue(link_with_alias_exists("a"))
        self.assertTrue(link_with_alias_exists("b"))
        self.assertTrue(link_with_alias_exists("custom-alias"))

        # These should not exist because we made them up
        self.assertFalse(link_with_alias_exists("banana"))
        self.assertFalse(link_with_alias_exists("random-fake-alias"))
        self.assertFalse(link_with_alias_exists("c"))


