def find_nonzero_max_max(g):
    return max(max(*g))
grid = [[0,0,0],[0,5,0],[0,0,0]]
print(find_nonzero_max_max(grid))  # Output: 5