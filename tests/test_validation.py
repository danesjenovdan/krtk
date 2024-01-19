from unittest import TestCase
from unittest.mock import patch
from validation import validate_shorten_link_payload


@patch("validation.link_with_alias_exists")
class TestValidation(TestCase):
    def test_validate_shorten_link_payload_valid_cases(self, mock_alias_exists):
        mock_alias_exists.return_value = False
        expected = validate_shorten_link_payload(
            {"destination": "http://www.example.com/test"}
        )
        self.assertEqual(expected, None)

        expected = validate_shorten_link_payload(
            {"destination": "http://www.example.com/test", "alias": "custom-alias"}
        )
        self.assertEqual(expected, None)

    def test_validate_shorten_link_payload_invalid_cases(self, mock_alias_exists):
        mock_alias_exists.return_value = False
        expected = validate_shorten_link_payload({})
        self.assertEqual(
            expected, {"destination": ["Missing data for required field."]}
        )

        expected = validate_shorten_link_payload(
            {"destination": "http://www.example.com/test", "alias": "🥰 is invalid"}
        )
        self.assertEqual(
            expected, {"alias": ["String does not match expected pattern."]}
        )

        expected = validate_shorten_link_payload(
            {"destination": "http://www.example.com/test", "foo": "bar"}
        )
        self.assertEqual(expected, {"foo": ["Unknown field."]})

        mock_alias_exists.return_value = True
        expected = validate_shorten_link_payload(
            {
                "destination": "http://www.example.com/test",
                "alias": "pre-existing-alias",
            }
        )
        self.assertEqual(
            expected, {"alias": ["Alias `pre-existing-alias` already in use."]}
        )
