# Crop a list of lists to height h and width w from top left corner
def crop_from_top_left(g, h, w):
    return [r[:w] for r in g[:h]]

# Test data
grid = [
    [1,2,3,4,5],
    [6,7,8,9,10],
    [11,12,13,14,15],
    [16,17,18,19,20],
    [21,22,23,24,25]
]

print("Original grid:")
print(grid)

# Test cropping to 3x3
result = crop_from_top_left(grid, 3, 3)
print("Cropped to 3x3:")
print(result)

# Test cropping to 2x4
result2 = crop_from_top_left(grid, 2, 4)
print("Cropped to 2x4:")
print(result2)