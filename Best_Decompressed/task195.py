def p(a):t=next((i for i,r in enumerate(a)if 5in r),0);d=min(r.index(5)for r in a if 5in r);return[[a[t+i//3*3][d+j//3*3]&a[t+i%3*3][d+j%3*3]for j in range(9)]for i in range(9)]
