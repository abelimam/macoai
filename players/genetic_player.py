import time
from typing import List
from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players.player import Player
from players.genetic.genetic_algorithm import GeneticAlgorithm, Chromosome


class GeneticPlayer(Player):
    def __init__(self, heuristic: Heuristic, population_size: int, mutation_rate: float, elite_rate: float, generations: int):
        super().__init__()
        self.heuristic = heuristic
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elite_rate = elite_rate
        self.generations = generations
        self.actions: List[Action] = []

    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        self.actions = []
        current_observation = observation.clone()

        chromosome_length = observation.get_game_parameters().get_action_points_per_turn()
        self.ga = GeneticAlgorithm(self.population_size, chromosome_length, self.mutation_rate, self.elite_rate)

        population = self.ga.initialize_population(current_observation)

        start_time = time.time()
        generation = 0
        best_fitness = float('-inf')

        while time.time() - start_time < budget:
            population = self.ga.evolve(population, self.fitness_function(current_observation, forward_model), current_observation)
            best_chromosome = max(population, key=lambda chromosome: chromosome.fitness)

            if best_chromosome.fitness > best_fitness:
                best_fitness = best_chromosome.fitness
                self.decode_chromosome(best_chromosome, current_observation, forward_model)

            generation += 1

        print(f"Generations: {generation}, Best Fitness: {best_fitness}")

    def fitness_function(self, observation: 'Observation', forward_model: 'ForwardModel'):
        def evaluate(chromosome: Chromosome) -> float:
            action_points = observation.get_game_parameters().get_action_points_per_turn()
            cloned_observation = observation.clone()
            cumulative_reward = 0.0

            for i in range(action_points):
                action = self.decode_gene(chromosome[i], cloned_observation)
                if action is not None and cloned_observation.is_action_valid(action):
                    forward_model.step(cloned_observation, action)
                    cumulative_reward += self.heuristic.get_reward(cloned_observation)
                else:
                    cumulative_reward -= 1.0  # Penalize invalid actions

            return cumulative_reward

        return evaluate

    def decode_gene(self, gene: int, observation: 'Observation') -> 'Action':
        actions = observation.get_actions()
        if 0 <= gene < len(actions):
            return actions[gene]
        else:
            return None

    def decode_chromosome(self, chromosome: Chromosome, observation: 'Observation',
                          forward_model: 'ForwardModel') -> None:
        action_points = observation.get_game_parameters().get_action_points_per_turn()
        for i in range(action_points):
            action = self.decode_gene(chromosome[i], observation)
            if action is not None and observation.is_action_valid(action):
                self.actions.append(action)
                forward_model.step(observation, action)

    def get_action(self, index: int) -> 'Action':
        if index < len(self.actions):
            return self.actions[index]
        return None

    def __str__(self):
        return "GeneticPlayer"