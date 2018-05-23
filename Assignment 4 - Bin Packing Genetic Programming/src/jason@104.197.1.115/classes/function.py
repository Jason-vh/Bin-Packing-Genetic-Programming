from helpers import debug
from .primitive import Primitive

print = debug('project:function')

class Function(Primitive):
  def __init__(self, symbol, arity, operation):
    self.operation = operation
    self._arity = arity
    super().__init__(symbol)

  def arity(self):
    return self._arity

  def evaluate(self, meta, args):
    try:
      return self.operation(*args)
    except ZeroDivisionError:
      return 1
    except OverflowError:
      return 1
    except ValueError:
      return 0

  def __str__(self):
    return f'Function {self.symbol}'