import re
from unittest import TestCase

from python_dice.src.syntax.open_parenthesis_syntax import OpenParenthesisSyntax


class TestOpenParenthesisSyntax(TestCase):
    def test_open_parenthesis_get_token_name(self):
        self.assertEqual(
            "OPEN_PARENTHESIS",
            OpenParenthesisSyntax.get_token_name(),
        )

    def test_open_parenthesis_get_token_regex(self):
        self.assertEqual(r"\(", OpenParenthesisSyntax.get_token_regex())

    def test_open_parenthesis_regex_will_match(self):
        test_cases = ["("]
        for test_case in test_cases:
            self.assertTrue(
                re.match(
                    OpenParenthesisSyntax.get_token_regex(),
                    test_case,
                ),
                f"did not match on case test_case {test_case}",
            )

    def testu_open_parenthesis_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "+", "*", "-", ")"]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(
                    OpenParenthesisSyntax.get_token_regex(),
                    test_case,
                ),
                f"matched on case test_case {test_case}",
            )
