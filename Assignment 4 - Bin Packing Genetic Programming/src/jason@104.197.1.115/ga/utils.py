import sys

def parse_file(filename: str):
  try:
    with open(filename, 'r') as file:
      data = file.read()
      data = data.split()
      return [data[0], data[1], data[2:]]
  except FileNotFoundError:
    print("Error: File not found", file=sys.stderr)
