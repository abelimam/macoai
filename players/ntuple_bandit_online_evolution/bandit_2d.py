from typing import Tuple
import math
import random

class Bandit2D:
    def __init__(self, c: float):
        """Class representing a 'bandit' that holds score data for a two-dimensional stat (an ordered pair), to be used in the model for the N-Tuple Bandit Online Evolution algorithm used"""
        self.C = c            # c parameter of the UCB equation
        self.score = dict()   # mean score of each element of the bandit
        self.n = dict()       # number of times that each element of the bandit has been accessed
        self.n_total = 0      # number of times that the bandit itself has been accessed
        self.factor = 1000    # a pair of elements [e1,e2] will be transformed to e1*factor+e2 to be an unique element
        # the factor needs to be bigger than the number of possible values per dimension

# region Methods
    def update(self, element1: int, element2: int, score: float) -> None:
        """Updates the bandit with a pair of elements and its score. If it doesn't exist yet, it is added."""
        element = self.get_element(element1, element2)   # From two elements to just one
        if element in self.score:
            self.score[element] = (self.score[element] * self.n[element] + score) / (self.n[element] + 1)
            self.n[element] += 1
        else:
            self.score[element] = score
            self.n[element] = 1
        self.n_total += 1

    def get_element(self, element1: int, element2: int) -> int:
        """Transforms a pair of elements int a unique individual element."""
        return element1 * self.factor + element2

    def get_elements(self, element: int) -> Tuple[int, int]:
        """Transforms an individual element back to the pair of elements in encodes."""
        element1 = element // self.factor
        element2 = element % self.factor
        return element1, element2
# endregion

# region Getters and Setters
    def get_score(self, element1: int, element2: int) -> float:
        """Returns the score of a given pair of elements."""
        element = self.get_element(element1, element2)
        return self.score[element]

    def get_ucb(self, element1: int, element2: int) -> float:
        """Returns the ucb value for a given pair of elements."""
        element = self.get_element(element1, element2)
        if element in self.score:
            return self.score[element] + self.C * math.sqrt(math.log(self.n_total) / self.n[element])
        else:
            return 10e6 + random.random()  # If the element is not in the bandit, return a random big number

    def get_elements_best_score(self) -> Tuple[int, int]:
        """Returns the pair of elements with the biggest score."""
        best_element = 0
        best_score = 0
        for element in self.score:
            if self.score[element] > best_score:
                best_score = self.score[element]
                best_element = int(element)
        element1, element2 = self.get_elements(best_element)
        return element1, element2

    def get_elements_best_ucb(self) -> Tuple[int, int]:
        """Returns the pair of elements with the biggest ucb value."""
        best_element = 0
        best_ucb = 0
        for element in self.score:
            element1, element2 = self.get_elements(element)
            ucb_value = self.get_ucb(element1, element2)
            if ucb_value > best_ucb:
                best_ucb = ucb_value
                best_element = int(element)
        element1, element2 = self.get_elements(best_element)
        return element1, element2
# endregion

# region Overrides
    def __repr__(self):
        return str(self.score) + " " + str(self.n)
# endregion