from unittest import TestCase

from PIL import Image  # type: ignore

from python_dice.src.probability_distribution.probability_distribution import ProbabilityDistribution
from python_dice.src.probability_distribution.probability_outcome_factory import ProbabilityOutcomeFactory
from python_dice.test import pil_image_to_byte_array

# pylint: disable=too-many-public-methods
from python_dice.test.test_image.test_image_path_finder import get_image_path


class TestProbabilityDistribution(TestCase):
    def setUp(self) -> None:
        self._probability_outcome_factory = ProbabilityOutcomeFactory()
        self._test_distribution_d4 = ProbabilityDistribution(
            self._probability_outcome_factory, {1: 1, 2: 1, 3: 1, 4: 1}
        )
        self._test_distribution_2 = ProbabilityDistribution(self._probability_outcome_factory, {2: 1})

    def test_probability_distribution_get_result_map(self):
        self.assertEqual({1: 1, 2: 1, 3: 1, 4: 1}, self._test_distribution_d4.get_result_map())

    def test_probability_distribution_get_dict_form(self):
        self.assertEqual(
            {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25},
            self._test_distribution_d4.get_dict_form(),
        )

    def test_probability_distribution_add(self):
        test_distribution_one = self._test_distribution_d4 + self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 + self._test_distribution_d4
        self.assertEqual({3: 1, 4: 1, 5: 1, 6: 1}, test_distribution_one.get_result_map())
        self.assertEqual(
            {2: 1, 3: 2, 4: 3, 5: 4, 6: 3, 7: 2, 8: 1},
            test_distribution_two.get_result_map(),
        )

    def test_probability_distribution_add_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4 + test_type

    def test_probability_distribution_sub(self):
        test_distribution_one = self._test_distribution_d4 - self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4
        self.assertEqual({-1: 1, 0: 1, 1: 1, 2: 1}, test_distribution_one.get_result_map())
        self.assertEqual(
            {-3: 1, -2: 2, -1: 3, 0: 4, 1: 3, 2: 2, 3: 1},
            test_distribution_two.get_result_map(),
        )

    def test_probability_distribution_sub_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4 - test_type

    def test_probability_distribution_mul(self):
        test_distribution_one = self._test_distribution_d4 * self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 * self._test_distribution_d4
        self.assertEqual({2: 1, 4: 1, 6: 1, 8: 1}, test_distribution_one.get_result_map())
        self.assertEqual(
            {1: 1, 2: 2, 3: 2, 4: 3, 6: 2, 8: 2, 9: 1, 12: 2, 16: 1},
            test_distribution_two.get_result_map(),
        )

    def test_probability_distribution_mul_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4 * test_type

    def test_probability_distribution_floordiv(self):
        test_distribution_one = self._test_distribution_d4 // self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 // self._test_distribution_d4
        self.assertEqual({0: 1, 1: 2, 2: 1}, test_distribution_one.get_result_map())
        self.assertEqual({0: 6, 1: 6, 2: 2, 3: 1, 4: 1}, test_distribution_two.get_result_map())

    def test_probability_distribution_floordiv_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4 // test_type

    def test_probability_distribution_max_operator(self):
        test_distribution_one = self._test_distribution_d4.max_operator(self._test_distribution_2)
        test_distribution_two = self._test_distribution_d4.max_operator(self._test_distribution_d4)
        self.assertEqual({2: 2, 3: 1, 4: 1}, test_distribution_one.get_result_map())
        self.assertEqual({1: 1, 2: 3, 3: 5, 4: 7}, test_distribution_two.get_result_map())

    def test_probability_distribution_max_operator_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4.max_operator(test_type)

    def test_probability_distribution_min_operator(self):
        test_distribution_one = self._test_distribution_d4.min_operator(self._test_distribution_2)
        test_distribution_two = self._test_distribution_d4.min_operator(self._test_distribution_d4)
        self.assertEqual({1: 1, 2: 3}, test_distribution_one.get_result_map())
        self.assertEqual({1: 7, 2: 5, 3: 3, 4: 1}, test_distribution_two.get_result_map())

    def test_probability_distribution_min_operator_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4.min_operator(test_type)

    def test_probability_distribution_max(self):
        test_distribution_one = self._test_distribution_d4 * self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4
        self.assertEqual(8, test_distribution_one.max())
        self.assertEqual(3, test_distribution_two.max())

    def test_probability_distribution_min(self):
        test_distribution_one = self._test_distribution_d4 * self._test_distribution_d4
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4
        self.assertEqual(1, test_distribution_one.min())
        self.assertEqual(-3, test_distribution_two.min())

    def test_probability_distribution_contains_zero(self):
        test_distribution_one = self._test_distribution_d4 * self._test_distribution_d4
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4
        self.assertEqual(False, test_distribution_one.contains_zero())
        self.assertEqual(True, test_distribution_two.contains_zero())

    def test_probability_distribution_average(self):
        test_distribution_one = self._test_distribution_d4 + self._test_distribution_d4
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4
        self.assertAlmostEqual(5, test_distribution_one.average(), delta=1e8)
        self.assertAlmostEqual(0, test_distribution_two.average(), delta=1e8)

    def test_probability_distribution_at_least(self):
        test_distribution_one = self._test_distribution_d4
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4

        least_one = test_distribution_one.at_least()
        least_two = test_distribution_two.at_least()

        self.assertAlmostEqual(1, least_one[1], delta=1e8)
        self.assertAlmostEqual(0.75, least_one[2], delta=1e8)
        self.assertAlmostEqual(0.5, least_one[3], delta=1e8)
        self.assertAlmostEqual(0.25, least_one[4], delta=1e8)

        self.assertAlmostEqual(1, least_two[-3], delta=1e8)
        self.assertAlmostEqual(6 / 7, least_two[-2], delta=1e8)
        self.assertAlmostEqual(5 / 7, least_two[-1], delta=1e8)
        self.assertAlmostEqual(4 / 7, least_two[0], delta=1e8)
        self.assertAlmostEqual(3 / 7, least_two[1], delta=1e8)
        self.assertAlmostEqual(2 / 7, least_two[2], delta=1e8)
        self.assertAlmostEqual(1 / 7, least_two[3], delta=1e8)

    def test_probability_distribution_at_most(self):
        test_distribution_one = self._test_distribution_d4
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4

        most_one = test_distribution_one.at_most()
        most_two = test_distribution_two.at_most()

        self.assertAlmostEqual(0.25, most_one[1], delta=1e8)
        self.assertAlmostEqual(0.5, most_one[2], delta=1e8)
        self.assertAlmostEqual(0.75, most_one[3], delta=1e8)
        self.assertAlmostEqual(1, most_one[4], delta=1e8)

        self.assertAlmostEqual(1 / 7, most_two[-3], delta=1e8)
        self.assertAlmostEqual(2 / 7, most_two[-2], delta=1e8)
        self.assertAlmostEqual(3 / 7, most_two[-1], delta=1e8)
        self.assertAlmostEqual(4 / 7, most_two[0], delta=1e8)
        self.assertAlmostEqual(5 / 7, most_two[1], delta=1e8)
        self.assertAlmostEqual(6 / 7, most_two[2], delta=1e8)
        self.assertAlmostEqual(1, most_two[3], delta=1e8)

    def test_probability_distribution_eq(self):
        test_distribution = self._test_distribution_d4.__equal__(self._test_distribution_d4)
        self.assertEqual({0: 12, 1: 4}, test_distribution.get_result_map())

    def test_probability_distribution_eq_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4.__equal__(test_type)

    def test_probability_distribution_ne(self):
        test_distribution = self._test_distribution_d4.__not_equal__(self._test_distribution_d4)
        self.assertEqual({0: 4, 1: 12}, test_distribution.get_result_map())

    def test_probability_distribution_ne_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4.__not_equal__(test_type)

    def test_probability_distribution_lt(self):
        test_distribution = self._test_distribution_d4 < self._test_distribution_d4
        self.assertEqual({0: 10, 1: 6}, test_distribution.get_result_map())

    def test_probability_distribution_lt_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4 < test_type

    def test_probability_distribution_le(self):
        test_distribution = self._test_distribution_d4 <= self._test_distribution_d4
        self.assertEqual({0: 6, 1: 10}, test_distribution.get_result_map())

    def test_probability_distribution_le_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4 <= test_type

    def test_probability_distribution_gt(self):
        test_distribution = self._test_distribution_d4 > self._test_distribution_d4
        self.assertEqual({0: 10, 1: 6}, test_distribution.get_result_map())

    def test_probability_distribution_gt_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4 > test_type

    def test_probability_distribution_ge(self):
        test_distribution = self._test_distribution_d4 >= self._test_distribution_d4
        self.assertEqual({0: 6, 1: 10}, test_distribution.get_result_map())

    def test_probability_distribution_ge_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4 >= test_type

    def test_probability_distribution_not_operator(self):
        test_distribution_d4_less_one = ProbabilityDistribution(
            self._probability_outcome_factory, {0: 1, 1: 1, 2: 1, 3: 1}
        )
        test_distribution = test_distribution_d4_less_one.not_operator()
        self.assertEqual({0: 3, 1: 1}, test_distribution.get_result_map())

    def test_probability_distribution_and(self):
        test_distribution_d2_less_one = ProbabilityDistribution(self._probability_outcome_factory, {0: 1, 1: 1})
        test_distribution = self._test_distribution_d4.__and__(test_distribution_d2_less_one)
        self.assertEqual({0: 4, 1: 4}, test_distribution.get_result_map())

    def test_probability_distribution_and_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4.__and__(test_type)

    def test_probability_distribution_or(self):
        test_distribution_d2_less_one = ProbabilityDistribution(self._probability_outcome_factory, {0: 1, 1: 1})
        test_distribution = test_distribution_d2_less_one.__or__(test_distribution_d2_less_one)
        self.assertEqual({0: 1, 1: 3}, test_distribution.get_result_map())

    def test_probability_distribution_or_non_probability_distribution(self):
        non_probability_distribution = {"int": 1, "str": "apple", "list": [1, 2], "set": {1, 2}, "dict": {1: 2, 3: 5}}
        for name, test_type in non_probability_distribution.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = self._test_distribution_d4.__or__(test_type)

    def test_probability_distribution_abs(self):
        test_distribution = ProbabilityDistribution(self._probability_outcome_factory, {-2: 2, -1: 1, 0: 1, 1: 1, 2: 3})
        abs_test_distribution = abs(test_distribution)
        self.assertEqual({0: 1, 1: 2, 2: 5}, abs_test_distribution.get_result_map())

    def test_get_histogram(self):
        test_distribution = ProbabilityDistribution(self._probability_outcome_factory, {1: 1, 2: 3, 3: 6, 4: 1})

        image_path = get_image_path(
            "TestProbabilityDistribution_test_get_histogram.tiff",
        )
        image = test_distribution.get_histogram()
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_get_at_least_histogram(self):
        test_distribution = ProbabilityDistribution(
            self._probability_outcome_factory, {2: 1, 3: 2, 4: 4, 5: 8, 6: 4, 7: 2, 8: 1}
        )
        image_path = get_image_path(
            "TestProbabilityDistribution_test_get_at_least_histogram.tiff",
        )
        image = test_distribution.get_at_least_histogram()
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_get_at_most_histogram(self):
        test_distribution = ProbabilityDistribution(self._probability_outcome_factory, {1: 1, 2: 3, 3: 6, 4: 1})
        image_path = get_image_path(
            "TestProbabilityDistribution_test_get_at_most_histogram.tiff",
        )
        image = test_distribution.get_at_most_histogram()
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_get_compare_histogram(self):
        test_distribution_one = ProbabilityDistribution(
            self._probability_outcome_factory, {1: 2, 2: 3, 3: 6, 4: 1, 5: 1}
        )
        test_distribution_two = ProbabilityDistribution(
            self._probability_outcome_factory, {0: 2, 1: 1, 2: 3, 3: 6, 4: 2}
        )
        image_path = get_image_path(
            "TestProbabilityDistribution_test_get_compare_histogram.tiff",
        )
        image = test_distribution_one.get_compare_histogram(test_distribution_two)
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_get_compare_at_least_histogram(self):
        test_distribution_one = ProbabilityDistribution(self._probability_outcome_factory, {1: 2, 2: 3, 3: 6, 4: 1})
        test_distribution_two = ProbabilityDistribution(self._probability_outcome_factory, {1: 1, 2: 3, 3: 6, 4: 7})
        image_path = get_image_path(
            "TestProbabilityDistribution_test_get_compare_at_least.tiff",
        )
        image = test_distribution_one.get_compare_at_least(test_distribution_two, "option 1", "option 2")
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_get_compare_at_most_histogram(self):
        test_distribution_one = ProbabilityDistribution(self._probability_outcome_factory, {1: 2, 2: 3, 3: 16, 4: 1})
        test_distribution_two = ProbabilityDistribution(self._probability_outcome_factory, {1: 1, 2: 3, 3: 6, 4: 2})
        image_path = get_image_path(
            "TestProbabilityDistribution_test_get_compare_at_most.tiff",
        )
        image = test_distribution_one.get_compare_at_most(test_distribution_two, "option a", "option b")
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_get_compare(self):
        test_distribution_one = ProbabilityDistribution(self._probability_outcome_factory, {1: 2, 2: 3, 3: 16, 4: 1})
        test_distribution_two = ProbabilityDistribution(self._probability_outcome_factory, {1: 1, 2: 3, 3: 6, 4: 2})
        image_path = get_image_path(
            "TestProbabilityDistribution_test_get_compare.tiff",
        )
        image = test_distribution_one.get_compare(test_distribution_two, "option a", "option b")
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_str(self):
        test_distribution = ProbabilityDistribution(self._probability_outcome_factory, {1: 2, 2: 3, 3: 16, 4: 1})
        self.assertEqual(
            "ProbabilityDistribution, result_map={ProbabilityOutcome: value=1, constraint_set=ConstraintSet: {"
            "NullConstraint}: 2, ProbabilityOutcome: value=2, constraint_set=ConstraintSet: {NullConstraint}: 3, "
            "ProbabilityOutcome: value=3, constraint_set=ConstraintSet: {NullConstraint}: 16, ProbabilityOutcome: "
            "value=4, constraint_set=ConstraintSet: {NullConstraint}: 1}",
            str(test_distribution),
        )

    def test_repr(self):
        test_distribution = ProbabilityDistribution(self._probability_outcome_factory, {1: 2, 2: 3, 3: 16, 4: 1})
        self.assertEqual(
            "ProbabilityDistribution, result_map={ProbabilityOutcome: value=1, constraint_set=ConstraintSet: {"
            "NullConstraint}: 2, ProbabilityOutcome: value=2, constraint_set=ConstraintSet: {NullConstraint}: 3, "
            "ProbabilityOutcome: value=3, constraint_set=ConstraintSet: {NullConstraint}: 16, ProbabilityOutcome: "
            "value=4, constraint_set=ConstraintSet: {NullConstraint}: 1}",
            repr(test_distribution),
        )
