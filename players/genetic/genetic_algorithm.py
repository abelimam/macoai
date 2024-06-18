import random
import numpy as np
from typing import List, Tuple
from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from collections import defaultdict



class GeneticAlgorithm:
    def __init__(self, heuristic: 'Heuristic', population_size: int, mutation_rate: float, elite_rate: float, forward_model_visits: int, visited_states: defaultdict):
        self.heuristic = heuristic
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elite_rate = elite_rate
        self.forward_model_visits = 0
        # self.visited_states = defaultdict(int)

    def generate_random_individual(self, observation: 'Observation', forward_model: 'ForwardModel') -> List['Action']:
        """Generates a random individual (a list of actions) based on the available actions."""
        individual = []
        current_observation = observation.clone()
        for _ in range(observation.get_game_parameters().get_action_points_per_turn()):
            actions = current_observation.get_actions()
            if actions:
                action = random.choice(actions)
                individual.append(action)
                forward_model.step(current_observation, action)
                self.forward_model_visits += 1
                # self.visited_states[current_observation] += 1
            else:
                break
        return individual

    def evaluate_individual(self, individual: List['Action'], observation: 'Observation',
                            forward_model: 'ForwardModel') -> float:
        """Evaluates the fitness of an individual by simulating the game with the individual's actions and the opponent's possible responses."""
        total_reward = 0
        num_simulations = 2

        for _ in range(num_simulations):
            new_observation = observation.clone()
            for action in individual:
                if forward_model.is_terminal(new_observation) or forward_model.is_turn_finished(new_observation):
                    break
                forward_model.step(new_observation, action)
                self.forward_model_visits += 1
                # self.visited_states[new_observation] += 1

            # Simulate the opponent's turn
            while not forward_model.is_turn_finished(new_observation):
                opponent_action = new_observation.get_random_action()
                forward_model.step(new_observation, opponent_action)
                self.forward_model_visits += 1
                # self.visited_states[new_observation] += 1

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

    def reproduce(self, parents: List[List['Action']], observation: 'Observation', forward_model: 'ForwardModel') -> \
    List[List['Action']]:
        """Creates offspring through crossover and mutation."""
        offspring = []
        for i in range(0, len(parents) - 1, 2):
            parent1, parent2 = parents[i], parents[i + 1]
            child1, child2 = self.crossover(parent1, parent2)
            child1 = self.mutate(child1, observation, forward_model)
            child2 = self.mutate(child2, observation, forward_model)
            offspring.extend([child1, child2])

        if len(parents) % 2 != 0:
            last_parent = parents[-1]
            last_child = self.mutate(last_parent, observation, forward_model)
            offspring.append(last_child)

        return offspring

    def crossover(self, parent1: List['Action'], parent2: List['Action']) -> Tuple[List['Action'], List['Action']]:
        """Performs crossover between two parents to create two children."""
        if len(parent1) <= 1 or len(parent2) <= 1:
            return parent1, parent2

        crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(self, individual: List['Action'], observation: 'Observation', forward_model: 'ForwardModel') -> List[
        'Action']:
        """Performs mutation on an individual."""
        mutated_individual = []
        current_observation = observation.clone()
        for action in individual:
            if random.random() < self.mutation_rate:
                actions = current_observation.get_actions()
                if actions:
                    mutated_action = random.choice(actions)
                    mutated_individual.append(mutated_action)
                    forward_model.step(current_observation, mutated_action)

                else:
                    mutated_individual.append(action)
                    forward_model.step(current_observation, action)
            else:
                mutated_individual.append(action)
                forward_model.step(current_observation, action)
            self.forward_model_visits += 1
            # self.visited_states[current_observation] += 1
        return mutated_individual