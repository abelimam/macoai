from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players.player import Player
import random
import numpy as np
from typing import List, Tuple


class GeneticPlayer(Player):
    def __init__(self, heuristic: 'Heuristic', population_size: int, mutation_rate: float, elite_rate: float, generations: int):
        super().__init__()
        self.heuristic = heuristic
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elite_rate = elite_rate
        self.generations = generations
        self.population = []
        self.turn = []

    # region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        """Computes a list of actions for a complete turn using a genetic algorithm and returns them in order each time it's called during the turn."""
        self.turn.clear()

        # Initialize population
        self.population = [self.generate_random_individual(observation) for _ in range(self.population_size)]

        for generation in range(self.generations):
            # Evaluate fitness of each individual
            fitness_scores = [self.evaluate_individual(individual, observation, forward_model) for individual in self.population]

            # Select parents for reproduction
            parents = self.select_parents(self.population, fitness_scores)

            # Create offspring through crossover and mutation
            offspring = self.reproduce(parents, observation)

            # Replace population with offspring, keeping the elite individuals
            elite_count = int(self.elite_rate * self.population_size)
            elite_individuals = [self.population[i] for i in np.argsort(fitness_scores)[-elite_count:]]
            self.population = elite_individuals + offspring[:self.population_size - elite_count]

        # Select the best individual as the action sequence for the turn
        best_individual = max(self.population, key=lambda individual: self.evaluate_individual(individual, observation, forward_model))
        self.turn = best_individual

    def get_action(self, index: int) -> 'Action':
        """Returns the next action in the turn."""
        if index < len(self.turn):
            return self.turn[index]
        return None

    def generate_random_individual(self, observation: 'Observation') -> List['Action']:
        """Generates a random individual (a list of actions) based on the available actions."""
        actions = observation.get_actions()
        individual = []
        for _ in range(observation.get_game_parameters().get_action_points_per_turn()):
            action = random.choice(actions)
            individual.append(action)
        return individual

    def evaluate_individual(self, individual: List['Action'], observation: 'Observation', forward_model: 'ForwardModel') -> float:
        """Evaluates the fitness of an individual by simulating the game with the individual's actions and the opponent's possible responses."""
        total_reward = 0
        num_simulations = 2

        for _ in range(num_simulations):
            new_observation = observation.clone()
            for action in individual:
                if forward_model.is_terminal(new_observation) or forward_model.is_turn_finished(new_observation):
                    break
                forward_model.step(new_observation, action)

            # Simulate the opponent's turn
            while not forward_model.is_turn_finished(new_observation):
                opponent_action = new_observation.get_random_action()
                forward_model.step(new_observation, opponent_action)

            reward = self.heuristic.get_reward(new_observation)
            total_reward += reward

        return total_reward / num_simulations

    def select_parents(self, population: List[List['Action']], fitness_scores: List[float]) -> List[List['Action']]:
        """Selects parents for reproduction based on their fitness scores."""
        parents = []
        for _ in range(self.population_size // 2):
            tournament_indices = random.sample(range(len(population)), 2)
            tournament_fitnesses = [fitness_scores[i] for i in tournament_indices]
            winner_index = tournament_indices[np.argmax(tournament_fitnesses)]
            parents.append(population[winner_index])
        return parents

    def reproduce(self, parents: List[List['Action']], observation: 'Observation') -> List[List['Action']]:
        """Creates offspring through crossover and mutation."""
        offspring = []
        for i in range(0, len(parents) - 1, 2):
            parent1, parent2 = parents[i], parents[i + 1]
            child1, child2 = self.crossover(parent1, parent2)
            child1 = self.mutate(child1, observation)
            child2 = self.mutate(child2, observation)
            offspring.extend([child1, child2])

        if len(parents) % 2 != 0:
            last_parent = parents[-1]
            last_child = self.mutate(last_parent, observation)
            offspring.append(last_child)

        return offspring

    def crossover(self, parent1: List['Action'], parent2: List['Action']) -> Tuple[List['Action'], List['Action']]:
        """Performs crossover between two parents to create two children."""
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(self, individual: List['Action'], observation: 'Observation') -> List['Action']:
        """Performs mutation on an individual."""
        mutated_individual = individual.copy()
        for i in range(len(mutated_individual)):
            if random.random() < self.mutation_rate:
                mutated_individual[i] = random.choice(observation.get_actions())
        return mutated_individual

    # endregion

    # region Override
    def __str__(self):
        return f"GeneticPlayer[{self.population_size}, {self.mutation_rate}, {self.elite_rate}, {self.generations}]"
    # endregion