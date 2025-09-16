q=lambda g:g if any(g[0]) else q(g[1:])
p=lambda g:q(q([*zip(*q(q([*zip(*g)])[::-1])[::-1])])[::-1])[::-1]