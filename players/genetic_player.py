from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players.player import Player
import random
import numpy as np
from typing import List, Tuple
from players.genetic import GeneticAlgorithm


class GeneticPlayer(Player):
    def __init__(self, heuristic: 'Heuristic', population_size: int, mutation_rate: float, elite_rate: float, generations: int = 100):
        super().__init__()
        self.heuristic = heuristic
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elite_rate = elite_rate
        self.generations = generations
        self.population = []
        self.turn = []
        self.genetic_algorithm = GeneticAlgorithm(self.heuristic, self.population_size, self.mutation_rate, self.elite_rate, self.forward_model_visits, self.visited_states)



    # region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        """Computes a list of actions for a complete turn using a genetic algorithm and returns them in order each time it's called during the turn."""
        self.turn.clear()

        # Initialize population
        self.population = [self.genetic_algorithm.generate_random_individual(observation, forward_model) for _ in range(self.population_size)]

        for generation in range(self.generations):
            # Evaluate fitness of each individual
            fitness_scores = [self.genetic_algorithm.evaluate_individual(individual, observation, forward_model) for individual in self.population]

            # Select parents for reproduction
            parents = self.genetic_algorithm.select_parents(self.population, fitness_scores)

            # Create offspring through crossover and mutation
            offspring = self.genetic_algorithm.reproduce(parents, observation, forward_model)

            # Replace population with offspring, keeping the elite individuals
            elite_count = int(self.elite_rate * self.population_size)
            elite_individuals = [self.population[i] for i in np.argsort(fitness_scores)[-elite_count:]]
            self.population = elite_individuals + offspring[:self.population_size - elite_count]

        # Select the best individual as the action sequence for the turn
        best_individual = max(self.population, key=lambda individual: self.genetic_algorithm.evaluate_individual(individual, observation, forward_model))
        self.turn = best_individual

        # Update forward_model_visits and visited_states from the GeneticAlgorithm instance
        self.forward_model_visits = self.genetic_algorithm.forward_model_visits
        # self.visited_states = self.genetic_algorithm.visited_states

    def get_action(self, index: int) -> 'Action':
        """Returns the next action in the turn."""
        if index < len(self.turn):
            return self.turn[index]
        return None

    # endregion

    # region Override
    def __str__(self):
        return f"GeneticPlayer[{self.population_size}, {self.mutation_rate}, {self.elite_rate}, {self.generations}]"
    # endregion
