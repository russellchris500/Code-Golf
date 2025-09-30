p=lambda g:[[*zip(*d[:15])]for l in(3,4,6,8)if(d:=(h:=[*zip(*g)])[:l]*6)[:(e:=g[4].index(0))]==h[:e]][0]
