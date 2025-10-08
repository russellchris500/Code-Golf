def p(d):n=len(d);return[[8if not d[a%n][f%n]and any(r[f%n]for r in d)else d[a%n][f%n]for f in range(2*n)]for a in range(2*n)]
