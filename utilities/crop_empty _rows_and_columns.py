# p crops the empty rows and columns on all edges
# this is longer than removing all empty rows and columns
q=lambda g:g if any(g[0])else q(g[1:])
p=lambda g:q(q([*zip(*q(q([*zip(*g)])[::-1])[::-1])])[::-1])[::-1]

#remove all empty rows and columns with this
p=lambda g:[*zip(*filter(any,zip(*filter(any,g))))]