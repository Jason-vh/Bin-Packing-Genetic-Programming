from helpers import debug
from ga import parse_file
from copy import deepcopy

print = debug('project:testcase')

class TestCase:
  def __init__(self, dataset, optimal_solution):
    print(f'Using test case {dataset}.')
    self.optimal_solution = optimal_solution
    self.number_items, self.bin_capacity, self.items = parse_file(f'../data/{dataset}')

  def getItems(self):
    return deepcopy(self.items)