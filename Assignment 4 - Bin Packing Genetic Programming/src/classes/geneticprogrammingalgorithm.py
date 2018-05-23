import random
import math

from graphviz import Graph

from helpers import debug
from .tree import Tree

print = debug('project:algorithm')

class Chromosome:
  tree: Tree
  fitness: float
  def __init__(self, tree):
    self.tree = tree
    self.fitness = float('inf')

  def mutate(self):
    random.choice([self.tree.mutate_grow, self.tree.mutate_function, self.tree.mutate_swap])()
    # self.tree.mutate_grow()
    # self.tree.mutate_function()
    # self.tree.mutate_terminal()
    # self.tree.mutate_swap()
    # self.tree.mutate_trunc()

class GeneticProgrammingAlgorithm():
  chromosomes: []
  def __init__(self, config):
    print(f'Initializing genetic programming algorithm')
    self.maximum_depth = config['maximum_tree_depth']
    self.population_size = config['population_size']
    self.function_set = config['function_set']
    self.terminal_set = config['terminal_set']
    self.iterations = config['iterations']

    self.chromosomes = []
    self.initialize_population()

  def initialize_population(self):
    print(f'Initializing population of size {self.population_size}')
    while len(self.chromosomes) < self.population_size:
      for depth in range(2, self.maximum_depth+1):
        if len(self.chromosomes) < self.population_size:
          tree = Tree.generate_tree(depth, 'GROW', self.function_set, self.terminal_set)
          self.chromosomes.append(Chromosome(tree))
        else:
          break

        if len(self.chromosomes) < self.population_size:

          tree = Tree.generate_tree(depth, 'FULL', self.function_set, self.terminal_set)
          self.chromosomes.append(Chromosome(tree))
        else:
          break

  def evolve(self, ga, test_cases):
    self.render()
    for iteration in range(self.iterations):
      print(f'Running iteration {iteration}')
      for chromosome in self.chromosomes:
        fitness_function = chromosome.tree
        chromosome.fitness = 0
        for test_case in test_cases:
          the_ga = ga(test_case.number_items, test_case.bin_capacity, test_case.getItems(), fitness_function)
          number_of_bins, best_fitness = the_ga.go()
          chromosome.fitness += (number_of_bins - test_case.optimal_solution)
          # print(f'There were {number_of_bins} bins with a fitness of {best_fitness}')
        chromosome.fitness /= len(test_cases)
        print(f'This fitness function has a fitness of {chromosome.fitness}')
      self.select()
      self.reproduce()
      self.mutate()

    best_chromosome = self.best_chromosome()
    self.render()
    print(f'The best chromosome was {best_chromosome.tree} with a fitness of {best_chromosome.fitness}')

  def render(self):
    graph = Graph(comment='All trees')

    for i in range(len(self.chromosomes)):
      tree = self.chromosomes[i].tree
      graph.subgraph(graph=tree.render(f'{i+1} [Original]'))

    graph.render('test-output/round-table.gv')

  def best_chromosome(self):
    self.chromosomes.sort(key=lambda c: c.fitness)
    return self.chromosomes[0]

  def select(self):
    winners = []
    N = round(len(self.chromosomes)/2)
    print(f'Selecting {N} winners')

    for _ in range(N):
      tournament = random.sample(self.chromosomes, 2)
      winner = min(tournament, key=lambda x: x.fitness)
      winners.append(winner)
      self.chromosomes.remove(winner)
    self.chromosomes = winners
    print(f'There are now {len(self.chromosomes)} chromosomes')

  def reproduce(self):
    couples = [self.chromosomes[i:i + 2] for i in range(0, len(self.chromosomes), 2)]
    for couple in couples:
      one, two = couple[0].tree.crossover(couple[1].tree)
      self.chromosomes.append(Chromosome(one))
      self.chromosomes.append(Chromosome(two))
    print('Chromosomes:')
    for c in self.chromosomes:
      print(c.tree)

  def mutate(self):
    # N = the number of chromosomes to be mutated
    N = math.ceil(0.33*len(self.chromosomes))
    to_be_mutated = random.sample(self.chromosomes, N)

    for chromosome in to_be_mutated:
      chromosome.mutate()