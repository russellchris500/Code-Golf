def rotate_clockwise(g):
    return [*zip(*g[::-1])]
# Example usage:
g = [[0,1,2],[3,4,5]]
print(rotate_clockwise(g))  # Output: [(3, 0), (4