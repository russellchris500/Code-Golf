#This function pads a 2d list of lists with zeros to the bottom and right
def pad(g,x,y):
   return [r+[0]*y for r in g]+[[0]*(len(g[0])+y)]*x

# Test data
grid = [
    [1, 2, 3],
    [4, 5, 6]
]

print("Original grid:")
for row in grid:
    print(row)
print()

# Test padding with 2 rows and 3 columns
result = pad(grid, 2, 3)
print("Padded with 2 rows, 3 cols:")
for row in result:
    print(row)
print()