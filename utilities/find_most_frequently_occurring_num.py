def p(g):
    return max(set(f:=sum(g,[])),key=f.count)