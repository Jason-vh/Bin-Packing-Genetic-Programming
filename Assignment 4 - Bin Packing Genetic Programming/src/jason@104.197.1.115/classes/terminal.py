import random
import string

from helpers import debug
from .primitive import Primitive

print = debug('project:terminal')

class Terminal(Primitive):
  symbols = []
  def __init__(self, symbol, description):
    self.symbol = symbol
    Terminal.symbols += symbol
    self.description = description
    self.value = 1

  def arity(self):
    return 0

  def evaluate(self, meta, args):
    return meta[self.symbol]

  def __str__(self):
    return f'Terminal {self.symbol}'

  def __int__(self):
    return self.value

class Constant(Terminal):
  def __init__(self):
    self.symbol = 'INVALID CONSTANT'
    self.name = 'A constant value'
    self.value = 'bob'

  def __call__(self):
    res = Constant()
    res.setValue(random.gauss(0, 10))
    return res

  def __int__(self):
    return self.value

  def evaluate(self, meta, args):
    return self.value

  def setValue(self, value):
    self.value = value
    self.symbol = str(round(value, 2))