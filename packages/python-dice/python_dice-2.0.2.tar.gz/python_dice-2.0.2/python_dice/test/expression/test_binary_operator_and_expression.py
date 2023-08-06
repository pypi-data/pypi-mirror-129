from unittest import TestCase
from unittest.mock import create_autospec

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.src.expression.binary_operator_expression import BinaryOperatorExpression
from python_dice.src.probability_distribution.probability_distribution_factory import ProbabilityDistributionFactory


class TestBinaryOperatorAndExpression(TestCase):
    def setUp(self):
        self._probability_distribution_factory = ProbabilityDistributionFactory()

        self._mock_syntax = [create_autospec(IDiceExpression) for _ in range(2)]
        self._mock_syntax[0].roll.return_value = 10
        self._mock_syntax[0].max.return_value = 8
        self._mock_syntax[0].min.return_value = 6
        self._mock_syntax[0].__str__.return_value = "7"
        self._mock_syntax[0].estimated_cost.return_value = 9
        self._mock_syntax[0].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {-3: 1, 0: 2, 4: 1}
        )
        self._mock_syntax[0].get_contained_variables.return_value = {"mock one"}

        self._mock_syntax[1].roll.return_value = 4
        self._mock_syntax[1].max.return_value = 6
        self._mock_syntax[1].min.return_value = 8
        self._mock_syntax[1].__str__.return_value = "2d8"
        self._mock_syntax[1].estimated_cost.return_value = 7
        self._mock_syntax[1].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {-3: 2, 0: 1, 1: 2, 4: 1}
        )
        self._mock_syntax[1].get_contained_variables.return_value = {"mock two"}

        self._test_binary_operator = BinaryOperatorExpression("AND", self._mock_syntax[0], self._mock_syntax[1])
        self._mock_parser_gen = create_autospec(rply.ParserGenerator)

    def test_binary_operator_add_production_function(self):
        BinaryOperatorExpression.add_production_function(self._mock_parser_gen, self._probability_distribution_factory)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : expression BINARY_OPERATOR expression"""
        )

    def test_and_roll_false(self):
        for _ in range(100):
            self.assertEqual(0, self._test_binary_operator.roll())

    def test_and_roll_true(self):
        self._mock_syntax[0].roll.return_value = 4
        for _ in range(100):
            self.assertEqual(1, self._test_binary_operator.roll())

    def test_and_max_true(self):
        self.assertEqual(1, self._test_binary_operator.max())

    def test_and_max_false(self):
        self._mock_syntax[0].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {-2: 1, -1: 2}
        )
        self._mock_syntax[1].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {0: 1}
        )

        self.assertEqual(0, self._test_binary_operator.max())

    def test_and_min_true(self):
        self._mock_syntax[0].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {4: 1}
        )
        self._mock_syntax[1].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {4: 1}
        )
        self.assertEqual(1, self._test_binary_operator.min())

    def test_and_min_false(self):
        self.assertEqual(0, self._test_binary_operator.min())

    def test_and_str(self):
        self.assertEqual("7 AND 2d8", str(self._test_binary_operator))

    def test_and_estimated_cost(self):
        self.assertEqual(16, self._test_binary_operator.estimated_cost())

    def test_and_get_probability_distribution(self):
        self.assertEqual(
            {0: 21, 1: 3},
            self._test_binary_operator.get_probability_distribution().get_result_map(),
        )

    def test_and_get_contained_variables(self):
        self.assertSetEqual(
            {"mock one", "mock two"},
            self._test_binary_operator.get_contained_variables(),
        )
