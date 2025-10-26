p=lambda g:[[((p:=min(k:=sum(g,[]),key=k.count))in{r[0],r[-1],c[0],c[-1]})*p for*c,in zip(*g)]for r in g]
