def p(i):
 return[[i[r//3][c//3]&i[r%3][c%3]for c in range(9)]for r in range(9)]