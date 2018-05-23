import random
import string

from graphviz import Graph

from helpers import debug
from .node import Node
from .terminal import Constant

print = debug('project:tree')

class Tree:
  root: Node
  maximum_depth: 0
  function_set: []
  terminal_set: []

  def __init__(self, root):
    self.root = root

  def print(self):
    self.root.print()

  def __str__(self):
    return self.root.print()



  @staticmethod
  def generate_tree(maximum_depth, policy, function_set, terminal_set):
    # print(f'Generating a tree with a maximum depth of {maximum_depth} and the {policy} policy')
    if policy.upper() == 'GROW':
      root = Node(random.choice(function_set + terminal_set)())
    elif policy.upper() == 'FULL':
      root = Node(random.choice(function_set)())

    tree = Tree(root)
    tree.root.generate_random_children(maximum_depth, function_set, terminal_set, policy)
    tree.function_set = function_set
    tree.terminal_set = terminal_set
    tree.maximum_depth = maximum_depth

    return tree

  def render(self, name):
    nodes = self.root.dfs()

    uid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    graph = Graph(comment='Generated tree', name= f'cluster{name}')
    graph.attr(label=f'Randomly Generated Tree {name} with value {round(self.evaluate({ "N": 10, "C": 2, "θ": 5}), 2)}')

    for i in range(len(nodes)):
      graph.node(uid+str(i), nodes[i].primitive.symbol)

    for i in range(len(nodes)):
      if nodes[i].parent is not None:
        graph.edge(uid+str(nodes.index(nodes[i].parent)), uid+str(i))

    return graph

  def evaluate(self, meta):
    return self.root.evaluate(meta)

  def getAllNodes(self):
    return self.root.dfs()

  def getFunctionNodes(self):
    return [n for n in self.getAllNodes() if n.primitive.arity() > 0]

  def getTerminalNodes(self):
    return [n for n in self.getAllNodes() if n.primitive.arity() == 0]

  # A node is replaced by a randomly generated subtree
  def mutate_grow(self):
    nodes = self.root.dfs()
    mutated_node = random.choice(nodes)
    mutated_node.primitive = random.choice(self.function_set + self.terminal_set)()
    mutated_node.children = []
    mutated_node.generate_random_children(self.maximum_depth, self.function_set, self.terminal_set, 'GROW')

  # Replace a random function node with a function of the same parity
  def mutate_function(self):
    nodes = self.getFunctionNodes()
    if len(nodes) > 0:
      node = random.choice(nodes)
      new_function = random.choice([f for f in self.function_set if f.arity() == node.primitive.arity()])()
      print(f'Replacing {node} with {new_function}')
      node.primitive = new_function

  # Replace a random terminal node with another random terminal node
  def mutate_terminal(self):
    node = random.choice(self.getTerminalNodes())
    new_terminal = random.choice(self.terminal_set)()
    print(f'Replacing {node} with {new_terminal}')
    node.primitive = new_terminal

  # Arguments of a random node are swapped
  def mutate_swap(self):
    nodes = self.getFunctionNodes()
    if len(nodes) > 0:

      mutated_node = random.choice(nodes)
      print(f'We are going to permutate {mutated_node}')

      if len(mutated_node.children) > 0:
        random.shuffle(mutated_node.children)

  def mutate_gaussian(self):
    constants = [n for n in self.getTerminalNodes() if isinstance(n.primitive,Constant)]
    print(f'There are {len(constants)} constants')
    if len(constants) > 0:
      node = random.choice(constants)
      print(f'The old value was {node}')
      node.primitive.setValue(node.primitive.value + random.gauss(0, 0.1))
      print(f'The new value is {node}')

  def mutate_trunc(self):
    nodes = self.getFunctionNodes()
    if len(nodes) > 0:
      node = random.choice(nodes)
      new_primitive = random.choice(self.terminal_set)()
      print(f'Node is changing from {node} to {new_primitive}')
      node.primitive = new_primitive
      node.children = []

  def clone(self):
    tree = Tree(self.root.clone())
    tree.function_set = self.function_set
    tree.terminal_set = self.terminal_set
    tree.maximum_depth = self.maximum_depth
    return tree


  def crossover(self, other):
    one, two = self.clone(), other.clone()
    node_one, node_two = random.choice(one.root.dfs()), random.choice(two.root.dfs())
    print(f'We are going to crossover on {node_one} and {node_two}')

    node_one.primitive, node_two.primitive = node_two.primitive, node_one.primitive
    node_one.children, node_two.children = node_two.children, node_one.children

    for c in node_one.children:
      c.parent = node_one

    for c in node_two.children:
      c.parent = node_two

    return one, two