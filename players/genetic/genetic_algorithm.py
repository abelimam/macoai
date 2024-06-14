import random
from typing import List, Tuple
from games import Observation, ForwardModel

class Chromosome:
    def __init__(self, genes: List[int]):
        self.genes = genes
        self.fitness = 0.0

    def __len__(self):
        return len(self.genes)

    def __getitem__(self, index):
        return self.genes[index]

    def __setitem__(self, index, value):
        self.genes[index] = value

class GeneticAlgorithm:
    def __init__(self, population_size: int, chromosome_length: int, mutation_rate: float, elite_rate: float, heuristic):
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.mutation_rate = mutation_rate
        self.elite_rate = elite_rate
        self.heuristic = heuristic


    def initialize_population(self, observation: 'Observation', forward_model: 'ForwardModel') -> List[Chromosome]:
        population = []
        for _ in range(self.population_size):
            genes = []
            for _ in range(self.chromosome_length):
                if random.random() < 0.0:  # 80% chance of selecting a heuristic-based action
                    action = self.select_heuristic_action(observation, forward_model)
                else:  # 20% chance of selecting a random action
                    action = random.randint(0, len(observation.get_actions()) - 1)
                genes.append(action)
            population.append(Chromosome(genes))
        return population

    def select_heuristic_action(self, observation: 'Observation', forward_model: 'ForwardModel') -> int:
        best_action_index = None
        best_score = float('-inf')

        for i, action in enumerate(observation.get_actions()):
            next_observation = observation.clone()
            forward_model.step(next_observation, action)
            score = self.heuristic.get_reward(next_observation)

            if score > best_score:
                best_score = score
                best_action_index = i

        return best_action_index

    def evaluate_fitness(self, population: List[Chromosome], fitness_function) -> None:
        for chromosome in population:
            chromosome.fitness = fitness_function(chromosome)

    def select_parents(self, population: List[Chromosome]) -> Tuple[Chromosome, Chromosome]:
        tournament_size = 10  
        tournament_candidates = random.sample(population, tournament_size)
        parent1 = max(tournament_candidates, key=lambda chromosome: chromosome.fitness)
        tournament_candidates = random.sample(population, tournament_size)
        parent2 = max(tournament_candidates, key=lambda chromosome: chromosome.fitness)
        return parent1, parent2

    def crossover(self, parent1: Chromosome, parent2: Chromosome, generation: int) -> Tuple[Chromosome, Chromosome]:
        if random.random() < 0.5:  # one-point crossover
            crossover_point = random.randint(1, len(parent1) - 1)
            child1_genes = parent1[:crossover_point] + parent2[crossover_point:]
            child2_genes = parent2[:crossover_point] + parent1[crossover_point:]
        else:  # uniform crossover
            child1_genes = []
            child2_genes = []
            for i in range(len(parent1)):
                if random.random() < 0.5:
                    child1_genes.append(parent1[i])
                    child2_genes.append(parent2[i])
                else:
                    child1_genes.append(parent2[i])
                    child2_genes.append(parent1[i])

        child1 = Chromosome(child1_genes)
        child2 = Chromosome(child2_genes)
        return child1, child2

    def mutate(self, chromosome: Chromosome, observation: 'Observation') -> None:
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                actions = observation.get_actions()
                if actions:
                    if random.random() < 0.5:
                        chromosome[i] = 1 - chromosome[i]
                    else:
                        chromosome[i] = random.randint(0, len(actions) - 1)

    def evolve(self, population: List[Chromosome], fitness_function, observation: 'Observation', generation: int) -> List[Chromosome]:
        self.evaluate_fitness(population, fitness_function)
        population = sorted(population, key=lambda chromosome: chromosome.fitness, reverse=True)
        elite_count = int(self.elite_rate * self.population_size)
        new_population = population[:elite_count]

        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents(population)
            child1, child2 = self.crossover(parent1, parent2, generation)
            self.mutate(child1, observation)
            self.mutate(child2, observation)
            new_population.extend([child1, child2])

        return new_population[:self.population_size]