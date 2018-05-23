import random

from helpers import debug
from .primitive import Primitive

print = debug('project:node')

class Node:
  primitive: Primitive
  children: []
  parent: None

  def __init__(self, primitive):
    self.primitive = primitive
    self.children = []
    self.parent = None

  def __str__(self):
    return str(self.primitive)

  def print(self):
    if len(self.children) == 2:
      return f'({self.children[0].print()} {self.primitive.symbol} {self.children[1].print()})'
    elif len(self.children) == 1:
      return f'({self.primitive.symbol} {self.children[0].print()})'
    else:
      return self.primitive.symbol

  def depth(self):
    if self.parent is None:
      return 1
    else:
      return 1 + self.parent.depth()

  def add_child(self, child):
    self.children.append(child)
    child.parent = self
    return child

  def generate_random_children(self, maximum_depth, function_set, terminal_set, policy):
    for _ in range(self.primitive.arity()):
      if self.depth() == 1:
        child = self.add_child(Node(random.choice(function_set)()))
        child.generate_random_children(maximum_depth, function_set, terminal_set, policy)
      elif self.depth() >= maximum_depth-1:
        self.add_child(Node(random.choice(terminal_set)()))
      else:
        if policy.upper() == 'GROW':
          child = self.add_child(Node(random.choice(terminal_set+function_set)()))
        elif policy.upper() == 'FULL':
          child = self.add_child(Node(random.choice(function_set)()))
        child.generate_random_children(maximum_depth, function_set, terminal_set, policy)

  def dfs(self):
    res = [self]
    for c in self.children:
      res += c.dfs()
    return res

  def evaluate(self, meta):
    return self.primitive.evaluate(meta=meta, args=list(map(lambda c: c.evaluate(meta), self.children)))

  def clone(self):
    node = Node(self.primitive())
    node.primitive.value = self.primitive.value
    for c in self.children:
      child = c.clone()
      node.children.append(child)
      child.parent = node
    return node


