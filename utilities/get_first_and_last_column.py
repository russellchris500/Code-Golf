def p(g):
    a,*_,c=zip(*g)
    return a,c

test = [[1,2,3],[4,5,6],[7,8,9]]
print(p(test))  # Output: ((1, 4, 7), (3, 6, 9))