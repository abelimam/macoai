from typing import List
from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players.online_evolution import TurnGenome
from players import Player
import time
import random

class OnlineEvolutionPlayer(Player):
    def __init__(self, heuristic: 'Heuristic', population_size: int, mutation_rate: float, survival_rate: float) -> None:
        """Entity that plays a game by using the Online Evolution algorithm to choose all actions in a turn."""
        super().__init__()
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.survival_rate = survival_rate
        self.heuristic = heuristic
        self.random_new_valid_action = False
        self.turn = []

    def set_random_new_valid_action(self, value = True):
        self.random_new_valid_action = value


# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        """Computes a list of actions for a complete turn using the Online Evolution algorithm and returns them in order each time it's called during the turn."""
        self.turn.clear()

        t0 = time.time()
        population: List['TurnGenome'] = []
        killed: List['TurnGenome'] = []

        new_observation = observation.clone()
        # initial population
        for i in range(self.population_size):
            genome = TurnGenome()
            observation.copy_into(new_observation)
            self.forward_model_visits += genome.random(new_observation, forward_model, self.visited_states)
            population.append(genome)
            killed.append(genome)

        while time.time() - t0 < budget - 0.1:
            # evaluate the new genomes
            for genome in killed:
                observation.copy_into(new_observation)
                for action in genome.get_actions():
                    forward_model.step(new_observation, action)
                    self.visited_states[new_observation] += 1
                    self.forward_model_visits += 1
                genome.set_reward(self.heuristic.get_reward(new_observation))

            # kill the worst genomes
            killed.clear()
            population.sort(key=lambda g: g.get_reward(), reverse=True)
            first_killed_genome_index = int(self.survival_rate * self.population_size)
            for i in range(first_killed_genome_index, self.population_size):
                killed.append(population[i])

            # create new genomes using the remaining ones for crossover
            for killed_genome in killed:
                # decide parents
                parent_a_index = random.randrange(first_killed_genome_index)
                parent_b_index = random.randrange(first_killed_genome_index)
                while parent_a_index == parent_b_index and len(killed) > 1:
                    parent_b_index = random.randrange(first_killed_genome_index)

                # crossover
                observation.copy_into(new_observation)
                self.forward_model_visits += killed_genome.\
                    crossover(population[parent_a_index], population[parent_b_index], new_observation, forward_model, self.visited_states)

                # mutate
                if random.random() < self.mutation_rate:
                    observation.copy_into(new_observation)
                    self.forward_model_visits += killed_genome.\
                        mutate_at_random_index(new_observation, forward_model, self.heuristic, self.random_new_valid_action, self.visited_states, self.verbose)

        # select the best genome to use for the turn
        self.turn = population[0].get_actions()

    def get_action(self, index: int) -> 'Action':
        """Returns the next action in the turn."""
        if index < len(self.turn):
            return self.turn[index]
        return None
# endregion

# region Override
    def __str__(self):
        return f"OnlineEvolutionPlayer[{self.population_size!s}][{self.mutation_rate!s}][{self.survival_rate!s}]"
# endregion