import colorama
import random

class debug:
  domains = {}

  def __init__(self, domain):
    self.domain = domain
    debug.domains[domain] = debug.domains[domain] if domain in debug.domains else random.choice(list(vars(colorama.Fore).values()))

  def __call__(self, s='', end='\n'):
    print(debug.domains[self.domain] + self.domain + colorama.Style.RESET_ALL + ' ' + str(s), end=end)