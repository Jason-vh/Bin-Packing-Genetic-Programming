from helpers import debug

print = debug('project:primitive')

class Primitive:
  def __init__(self, symbol):
    self.symbol = symbol
    self.value = 'empty'

  def arity(self):
    raise NotImplementedError

  def evaluate(self, meta, args):
    raise NotImplementedError

  def __call__(self):
    return self