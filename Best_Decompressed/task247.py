def p(g):b=sum(g,[]);c=max(b.count(x)for x in b if x>0);return[[x for x in dict.fromkeys(sum(zip(*g[::-1]),()))if b.count(x)==c]]*c
