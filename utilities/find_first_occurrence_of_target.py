#This code finds the first occurrence of a target value in a 2D grid and returns its coordinates (row, column).
def find_first(g, t):
    return divmod(sum(g,[]).index(t),len(g[0]))
# Test data
grid = [[1,2,3],[4,5,6],[7,8,9]]
target = 5
print(find_first(grid, target))  # Output: (1, 1)