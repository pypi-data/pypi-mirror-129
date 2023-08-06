from unittest import TestCase
from unittest.mock import create_autospec

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.src.expression.multiply_expression import MultiplyExpression
from python_dice.src.probability_distribution.probability_distribution_factory import ProbabilityDistributionFactory


class TestMultiplyExpression(TestCase):
    def setUp(self):
        self._probability_distribution_factory = ProbabilityDistributionFactory()

        self._mock_syntax = [create_autospec(IDiceExpression) for _ in range(2)]
        self._mock_syntax[0].roll.return_value = 10
        self._mock_syntax[0].max.return_value = 8
        self._mock_syntax[0].min.return_value = 2
        self._mock_syntax[0].__str__.return_value = "7"
        self._mock_syntax[0].estimated_cost.return_value = 9
        self._mock_syntax[0].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {-2: 1, 4: 1}
        )
        self._mock_syntax[0].get_contained_variables.return_value = {"mock one"}

        self._mock_syntax[1].roll.return_value = 4
        self._mock_syntax[1].max.return_value = 6
        self._mock_syntax[1].min.return_value = 8
        self._mock_syntax[1].__str__.return_value = "2"
        self._mock_syntax[1].estimated_cost.return_value = 7
        self._mock_syntax[1].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {8: 1, -3: 2}
        )
        self._mock_syntax[1].get_contained_variables.return_value = {"mock two"}

        self._test_multiply = MultiplyExpression(self._mock_syntax[0], self._mock_syntax[1])
        self._mock_parser_gen = create_autospec(rply.ParserGenerator)

    def test_multiply_add_production_function(self):
        MultiplyExpression.add_production_function(self._mock_parser_gen, self._probability_distribution_factory)
        self._mock_parser_gen.production.assert_called_once_with("""expression : expression MULTIPLY expression""")

    def test_multiply_roll(self):
        for _ in range(100):
            self.assertEqual(40, self._test_multiply.roll())

    def test_multiply_max(self):
        self.assertEqual(32, self._test_multiply.max())

    def test_multiply_min(self):
        self.assertEqual(-16, self._test_multiply.min())

    def test_multiply_str(self):
        self.assertEqual("7 * 2", str(self._test_multiply))

    def test_multiply_estimated_cost(self):
        self.assertEqual(16, self._test_multiply.estimated_cost())

    def test_multiply_get_probability_distribution(self):
        self._mock_syntax[0].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {10: 1, -12: 2, 0: 1}
        )
        self._mock_syntax[1].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {2: 1, 3: 2}
        )
        self.assertEqual(
            {-36: 4, -24: 2, 0: 3, 20: 1, 30: 2},
            self._test_multiply.get_probability_distribution().get_result_map(),
        )

    def test_multiply_get_contained_variables(self):
        self.assertSetEqual({"mock one", "mock two"}, self._test_multiply.get_contained_variables())
