# Of course you should use these in line, not as functions or lambdas

# Find the number of colors in a list
def num_colors(l):
    return len(set(l))

# Transpose a 2d grid
# Caution: returns a list of tuples, not a list of lists
def transpose(g):
    return [*zip(*g)] # you can use "zip(*g)"" if you need an iterator

# Flatten a 2d grid to a 1d list
def flatten(g):
    return sum(g,[])