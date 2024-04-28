import random
import math

class Bandit1D:
    def __init__(self, c: float):
        """Class representing a 'bandit' that holds score data for a one-dimensional stat, to be used in the model for the N-Tuple Bandit Online Evolution algorithm used"""
        self.C = c            # c parameter of the UCB equation
        self.score = dict()   # mean score of each element of the bandit
        self.n = dict()       # number of times that each element of the bandit has been accessed
        self.n_total = 0      # number of times that the bandit itself has been accessed

# region Methods
    def update(self, element: int, score: float) -> None:
        """Updates the bandit with an element and its score. If it doesn't exist yet, it is added."""
        if element in self.score:
            self.score[element] = (self.score[element] * self.n[element] + score) / (self.n[element] + 1)
            self.n[element] += 1
        else:
            self.score[element] = score
            self.n[element] = 1
        self.n_total += 1
# endregion

# region Getters and Setters
    def get_score(self, element: int) -> float:
        """Returns the score of the given element."""
        return self.score[element]

    def get_ucb(self, element: int) -> float:
        """Returns the ucb value for a given element."""
        if element in self.score:
            return self.score[element] + self.C * math.sqrt(math.log(self.n_total) / self.n[element])
        else:
            return 10e6 + random.random()  # If the element is not in the bandit, return a random big number

    def get_ucb_final(self, element: int) -> float:
        """Returns the ucb value for a given element. If not exists, returns 0."""
        if element in self.score:
            return self.score[element] + self.C * math.sqrt(math.log(self.n_total) / self.n[element])
        else:
            return 0.0

    def get_element_best_score(self) -> int:
        """Returns the element with the biggest score."""
        best_element = 0
        best_score = 0
        for element in self.score:
            if self.score[element] > best_score:
                best_score = self.score[element]
                best_element = int(element)
        return best_element

    def get_element_best_ucb(self) -> int:
        """Returns the element with the biggest ucb value."""
        best_element = 0
        best_ucb = 0
        for element in self.score:
            ucb_value = self.get_ucb(element)
            if ucb_value > best_ucb:
                best_ucb = ucb_value
                best_element = int(element)
        return best_element
# endregion

# region Overrides
    def __repr__(self):
        return str(self.score) + " " + str(self.n)
# endregion