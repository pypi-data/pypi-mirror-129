from abc import ABC, abstractmethod
from typing import Tuple

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)


class IPythonDiceParser(ABC):
    @abstractmethod
    def parse(
        self,
        input_text: str,
        state: IProbabilityDistributionState = None,
    ) -> Tuple[IDiceExpression, IProbabilityDistributionState]:
        """

        :return: output of pydice program
        """
