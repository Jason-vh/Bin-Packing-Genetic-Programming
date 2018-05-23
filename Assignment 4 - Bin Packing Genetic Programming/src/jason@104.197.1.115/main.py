from helpers import debug
from classes import GeneticProgrammingAlgorithm, Function, Terminal, Constant, TestCase
from ga import HGGA, parse_file

import math

import os

# Config
MAXIMUM_TREE_DEPTH = 5
POPULATION = 8
ITERATIONS = 10

# Clear the console
os.system('clear')

# Initialize debug
print = debug('project:main')

if __name__ == "__main__":
  print('Initializing')

  possible_functions = [
    Function('*', 2, lambda a,b: a*b),
    Function('+', 2, lambda a,b: a+b),
    Function('-', 2, lambda a,b: a-b),
    Function('/', 2, lambda a,b: a/b),
    Function('√', 1, lambda a: math.sqrt(a)),
    Function('^2', 1, lambda a: pow(a, 2)),
    # Function('pow', 2, lambda a,b: a**b)
  ]

  possible_terminals = [
    Terminal('N', 'Number of bins'),
    Terminal('C', 'capacity of bins'),
    Terminal('θ', 'Overall bin fullness'),
    Constant()
  ]

  test_cases = [
    TestCase('easy/N1C1W1_A.BPP', 25),
    TestCase('easy/N1C1W1_B.BPP', 31),
    # TestCase('easy/N1C1W1_C.BPP', 20),
    # TestCase('easy/N1C1W1_D.BPP', 28)
  ]

  config = {
    'maximum_tree_depth': MAXIMUM_TREE_DEPTH,
    'population_size': POPULATION,
    'function_set': possible_functions,
    'terminal_set': possible_terminals,
    'iterations': ITERATIONS
  }

  gpa = GeneticProgrammingAlgorithm(config)
  gpa.evolve(HGGA, test_cases)
