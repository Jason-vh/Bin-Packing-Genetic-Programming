from random import shuffle, choice, sample, uniform
from copy import deepcopy
from math import ceil
import time
from csv import writer
from helpers import debug

print = debug('project:hgga')

POPULATION = 40
TOURNAMENT_SIZE = 4
ITERATIONS = 200
UNCHANGED_ITERATIONS = 100

crossover_time = 0
mutation_time = 0

class Item:
  def __init__(self, weight, id):
    self.weight = int(weight)
    self.id = id

  def __eq__(self, other):
    return self.id == other.id

  def __str__(self):
    return f"{self.id}"

class Bin:
  def __init__(self, capacity):
    self.items = []
    self.capacity = capacity

  def can_hold(self, item):
    return (self.weight() + item.weight) <= self.capacity

  def add_item(self, item):
    self.items.append(item)

  def weight(self):
    return sum(map(lambda i: i.weight, self.items))

  def contains(self, item):
    return item in self.items

  def try_replace(self, n, item):
    self.items.sort(key = lambda i: i.weight)

    for i in range(0, len(self.items)-n):
      total_weight = sum(map(lambda i: i.weight, self.items[i:i+n]))
      new_weight = self.weight() - total_weight + item.weight
      if new_weight <= self.capacity and new_weight >= self.weight():
        removed_items = self.items[i:i+n]
        self.items[i:i+n] = [item]
        return removed_items
    return False

  def __str__(self):
    return '[' + ', '.join(map(str, self.items)) + ']'

class Chromosome:
  def __init__(self, items, bin_capacity, fitness_function):
    self.bin_capacity = bin_capacity
    self.bins = [Bin(self.bin_capacity)]
    self.fitness_function = fitness_function
    shuffle(items)

    for item in items:
      self.add_item(item)

  def add_item(self, item):
    for bin in self.bins:
      if bin.can_hold(item):
        bin.add_item(item)
        return

    self.bins.append(Bin(self.bin_capacity))
    self.add_item(item)

  def total_items(self):
    return sum(map(lambda b: len(b.items), self.bins))

  def __str__(self):
    return '\n'.join(map(str, self.bins))

  def fitness(self):
    meta = { 'N': len(self.bins), 'C': self.bin_capacity, 'θ': sum(map(lambda b: (b.weight()/self.bin_capacity), self.bins)) }
    return self.fitness_function.evaluate(meta)
    # N, C, k = len(self.bins), self.bin_capacity, 2
    # theta = sum(map(lambda b: (b.weight()/C)**k, self.bins))
    # return theta/N

  def crossover_with(self, other):
    starting_items = self.total_items()

    # Make a copy of the child
    child = self
    child.bins = list(map(deepcopy, self.bins))

    # Get the crossover points
    points = sorted([ choice(range(len(child.bins))), choice(range(len(other.bins))) ])

    # Get the bins to be injected
    bins = list(map(deepcopy, other.bins[points[0]:points[1]]))

    # Remove bins with duplicate items
    removed_items = []
    for injected_bin in bins:
      for item in injected_bin.items:
        item = deepcopy(item)
        for child_bin in child.bins:
          if child_bin.contains(item):
            removed_items.extend(child_bin.items)
            child.bins.remove(child_bin)
            continue

    for b in bins:
      removed_items = [item for item in removed_items if not b.contains(item)]
    removed_items.sort(key=lambda item: item.weight)

    # Inject the bins
    child.bins[points[0]:points[0]] = list(map(deepcopy, bins))

    # Add removed items
    child.smart_replace(removed_items)

    for item in removed_items:
      child.add_item(item)

    if starting_items != child.total_items():
      print(f'Warning: Number of items changed during crossover. Before: {starting_items}, after: {child.total_items()}')

    return deepcopy(child)

  def mutate(self):
    # Copy the original bins
    original_bins = list(map(deepcopy, self.bins))
    original_fitness = self.fitness()

    # p is the mutation chance
    p = 0.5
    removed_items = []

    # Randomly remove bins
    for b in self.bins:
      if uniform(0, 1) > p:
        removed_items.extend(b.items)
        self.bins.remove(b)

    # Insert removed items
    removed_items.sort(key = lambda item: item.weight)

    self.smart_replace(removed_items)

    for item in removed_items:
      self.add_item(item)

    if self.fitness() >= original_fitness:
      return
    else:
      self.bins = original_bins

  def smart_replace(self, items):
    for i in range(len(items)):
      has_replaced = False
      item = items[i]
      for bin in self.bins:
        res = bin.try_replace(3, item)
        if res:
          items[i:i+1] = res
          has_replaced = True
          break
      if has_replaced:
        break


    for i in range(len(items)):
      has_replaced = False
      item = items[i]
      for bin in self.bins:
        res = bin.try_replace(2, item)
        if res:
          items[i:i+1] = res
          has_replaced = True
          break
      if has_replaced:
        break

class HGGA:
  def __init__(self, number_items, bin_capacity, _items, fitness_function):
    bin_capacity = int(bin_capacity)
    items = []
    id = 1
    for item in _items:
      items.append(Item(item, id))
      id += 1

    # print("Initializing HGGA...")
    print(f'Using fitness function: {fitness_function}')
    self.number_items = number_items
    self.bin_capacity = bin_capacity
    self.fitness_function = fitness_function
    # print(f"Number of items: {number_items}")
    # print(f"Bin capacity: {bin_capacity}")
    self.chromosomes = list(map(lambda _: Chromosome(deepcopy(items), bin_capacity, fitness_function), [None]*POPULATION))
    # print(f"Initialized {len(self.chromosomes)} chromosomes")
    print()

  def select(self):
    winners = []
    N = round(len(self.chromosomes)/2) # The number of parents to be selected

    for _ in range(N):
      tournament = sample(self.chromosomes, TOURNAMENT_SIZE)
      winner = max(tournament, key=lambda x: x.fitness())
      winners.append(winner)
      self.chromosomes.remove(winner)

    self.chromosomes = winners

  def crossover(self):
    couples = [self.chromosomes[i:i + 2] for i in range(0, len(self.chromosomes), 2)]
    for couple in couples:
      self.chromosomes.append(deepcopy(couple[0]).crossover_with(deepcopy(couple[1])))
      self.chromosomes.append(deepcopy(couple[1]).crossover_with(deepcopy(couple[0])))

  def mutate(self):
    # N = the number of chromosomes to be mutated
    N = ceil(0.66*len(self.chromosomes))
    to_be_mutated = sample(self.chromosomes, N)

    for chromosome in to_be_mutated:
      chromosome.mutate()

  def go(self):
    # csv_file = open("stats.csv", "a")
    # csv_writer = writer(csv_file)
    current_best_fitness = 0
    current_iterations = 0

    for _ in range(ITERATIONS):
      self.chromosomes.sort(key = lambda c: c.fitness(), reverse=True)
      fitness = self.chromosomes[0].fitness()

      print(f"\rRunning{'.'* (_ %4)}         \r", end='')

      if abs(fitness-current_best_fitness) > 0.01:
        current_iterations = 0
        current_best_fitness = fitness
      else:
        current_iterations += 1

      if current_iterations >= UNCHANGED_ITERATIONS:
        break

      self.select()
      self.crossover()
      self.mutate()

    self.chromosomes.sort(key = lambda c: c.fitness(), reverse=True)
    return len(self.chromosomes[0].bins), self.chromosomes[0].fitness()
    # print(f"The optimal solution has {len(self.chromosomes[0].bins)} bins with a fitness of {self.chromosomes[0].fitness()}. {self.chromosomes[0].total_items()}")
    # csv_file.close()