vars = {}
env = lambda key: vars.get(key)
path = '.env'

with open(path, 'r') as f:
    for line in f:
        var, value = line.strip().split('=', 1)
        vars[var] = value