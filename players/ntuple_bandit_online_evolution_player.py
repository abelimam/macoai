from typing import Tuple, List
from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players.ntuple_bandit_online_evolution import Bandit1D, Bandit2D, FitnessEvaluator
from players import Player
import copy
import math
import random
import time

class NTupleBanditOnlineEvolutionPlayer(Player):
    def __init__(self, heuristic: 'Heuristic', fitness: 'FitnessEvaluator', dimensions: List[int], c_value: float,
                 neighbours: int, mutation_rate: float, initializations: int):
        """Entity that plays a Game by using the N-Tuple Bandit Online Evolution to model fitness and evolve a list of Action based on it, composing a turn."""
        super().__init__()
        self.c_value = c_value  # c parameter for UCB
        self.neighbours = neighbours  # amount of neighbours per iteration
        self.mutation_rate = mutation_rate
        self.initializations = initializations

        self.dimensions = dimensions  # possible values per parameter
        self.dimension_amount = len(dimensions)  # dimensions of the problem to solve

        self.bandits1D: List['Bandit1D'] = []  # 1D bandits
        self.bandits2D: List['Bandit2D']  = []  # 2D bandits
        self.bandit1D_amount = self.dimension_amount  # amount of 1D bandits
        self.bandit2D_amount = (self.dimension_amount * (self.dimension_amount - 1)) / 2  # amount of 2D bandits

        self.create_bandits()  # initialize the 1D and 2D bandits
        self.fitness = fitness
        self.heuristic = heuristic

        self.currents = []  # list of the selected individuals
        self.turn = []  # selected turn to play

# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        """Computes a list of Action for a complete turn using the N-Tuple Bandit Online Evolution and returns them in order each time it's called during the turn."""
        self.turn.clear()
        self.bandits1D.clear()
        self.bandits2D.clear()
        self.create_bandits()
        self.currents.clear()
        self.turn.clear()

        t0 = time.time()
        current, score = self.valid_initialization(observation, forward_model, self.initializations)
        new_observation = observation.clone()
        while time.time() - t0 < budget - 0.01:
            population = self.get_neighbours(current, self.neighbours, self.mutation_rate)
            new_current = self.get_best_individual(population)
            observation.copy_into(new_observation)
            new_score = self.fitness.evaluate(new_current, new_observation, forward_model, self.visited_states)
            self.forward_model_visits += len(new_current)
            if new_score > score:
                current = new_current
                score = new_score
            self.update_bandits(new_current, new_score)
        self.turn = self.fitness.ntboe_to_turn(current)

    def get_action(self, index: int) -> 'Action':
        """Returns the next action in the turn."""
        if index < len(self.turn):
            return self.turn[index]
        return None

    def create_bandits(self) -> None:
        """Create the empty 1D and 2D bandits."""
        # Create empty 1D bandits
        for i in range(self.dimension_amount):
            new_bandit = Bandit1D(self.c_value)
            self.bandits1D.append(new_bandit)

        # Create empty 2D bandits
        for i in range(0, self.dimension_amount - 1):
            for j in range(i + 1, self.dimension_amount):
                new_bandit = Bandit2D(self.c_value)
                self.bandits2D.append(new_bandit)

    def valid_initialization(self, observation: 'Observation', forward_model: 'ForwardModel', initializations: int) -> Tuple[List[int], float]:
        """Generates a given amount of complete valid turns randomly and adds their stats to the bandit-based model, returning the best turn found and the score it yielded."""
        population = []
        best_individual = None
        best_score = -math.inf
        new_observation = observation.clone()
        for i in range(initializations):
            observation.copy_into(new_observation)
            individual = self.get_random_individual_valid(new_observation, forward_model)
            population.append(individual)
            score = self.heuristic.get_reward(new_observation)
            self.update_bandits(individual, score)  # Update bandits
            if score > best_score:
                best_score = score
                best_individual = individual
        return best_individual, best_score

    def get_random_individual_valid(self, observation: 'Observation', forward_model: 'ForwardModel') -> List[int]:
        """Generates a random turn that is valid for the given observation. Note that the observation state after running this method will be the result of playing the turn."""
        individual = []
        for i in range(self.dimension_amount):
            act = observation.get_random_action()
            n = self.fitness.get_parameter_from_action(act)
            individual.append(n)
            forward_model.step(observation, act)
            self.visited_states[observation] += 1
            self.forward_model_visits += 1
        return individual

    def update_bandits(self, individual: List[int], score: float) -> None:
        """Updates the bandits with the given individual and score."""
        # 1D
        for i in range(self.bandit1D_amount):
            element = individual[i]
            self.bandits1D[i].update(element, score)

        # 2D
        k = 0
        for i in range(0, self.dimension_amount - 1):
            for j in range(i + 1, self.dimension_amount):
                element1 = individual[i]
                element2 = individual[j]
                self.bandits2D[k].update(element1, element2, score)
                k += 1

    def get_neighbours(self, individual: List[int], neighbour_amount: int, mutation_rate: float) -> List[List[int]]:
        """Generates a list of neighbours from an individual. It changes at least one parameter (randomly chosen). The rest of them can change depending on the mutation rate."""
        population = []
        while len(population) < neighbour_amount:
            neighbour = copy.copy(individual)
            i = random.randint(0, self.dimension_amount - 1)
            for j in range(self.dimension_amount):
                if i == j:  # The parameter chosen is always mutated
                    self.mutate_gen(neighbour, j)
                else:  # The rest of them may be mutated depending on the mutation prob.
                    n = random.random()
                    if n < mutation_rate:
                        self.mutate_gen(neighbour, j)
            if neighbour not in population:
                if neighbour not in self.currents:
                    population.append(neighbour)
        return population

    def mutate_gen(self, individual: List[int], j: int) -> None:
        """Mutate the j-th gen of an individual."""
        prev_value = individual[j]
        new_value = random.randint(0, self.dimensions[j] - 1)
        while new_value == prev_value:  # if it is the same, try again
            new_value = random.randint(0, self.dimensions[j] - 1)
        individual[j] = new_value

    def get_best_individual(self, population: List[List[int]]) -> List[int]:
        """Returns the best individual from a population, by UCB"""
        best_ucb = -math.inf
        best_individual = population[0]

        for individual in population:
            ucb = self.get_total_ucb(individual)
            if ucb > best_ucb:
                best_ucb = ucb
                best_individual = individual

        return best_individual

    def get_total_ucb(self, individual: List[int]) -> float:
        """Returns the UCB of an individual, being the mean of its UCB for each bandit. If the individual is not in a bandit it will return a big number."""
        acm = 0
        # 1D
        for i in range(0, self.dimension_amount):
            element = individual[i]
            acm += self.bandits1D[i].get_ucb(element)
            i += 1

        # 2D
        k = 0
        for i in range(0, self.dimension_amount - 1):
            for j in range(i + 1, self.dimension_amount):
                element1 = individual[i]
                element2 = individual[j]
                acm += self.bandits2D[k].get_ucb(element1, element2)
                k += 1

        return acm / (self.bandit1D_amount + self.bandit2D_amount)
# endregion

# region Overrides
    def __str__(self):
        return f"NTupleBanditOnlineEvolution[{self.c_value}][{self.neighbours}][{self.mutation_rate}][{self.initializations}]"
# endregion
