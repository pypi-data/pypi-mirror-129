import re
from unittest import TestCase

from python_dice.src.syntax.binary_operator_syntax import BinaryOperatorSyntax


class TestBinaryOperatorSyntax(TestCase):
    def test_binary_operator_syntax_get_token_name(self):
        self.assertEqual(
            "BINARY_OPERATOR",
            BinaryOperatorSyntax.get_token_name(),
        )

    def test_binary_operator_syntax_get_token_regex(self):
        self.assertEqual(
            r"==|!=|<=|<|>=|>|\bAND\b|\bOR\b",
            BinaryOperatorSyntax.get_token_regex(),
        )

    def test_binary_operator_syntax_regex_will_match(self):
        test_cases = ["==", "!=", "<", "<=", ">", ">=", "AND", "OR"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(
                    BinaryOperatorSyntax.get_token_regex(),
                    test_case,
                ),
                f"did not match on case test_case {test_case}",
            )

    def test_binary_operator_syntax_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "-", "+", "(", "!"]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(
                    BinaryOperatorSyntax.get_token_regex(),
                    test_case,
                ),
                f"matched on case test_case {test_case}",
            )
