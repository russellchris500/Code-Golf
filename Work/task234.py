def p(g):
	T=len(g);U=len(g[0]);C={}
	for A,j in enumerate(g):
		for B,I in enumerate(j):
			if I:C.setdefault(I,set()).add((A,B))
	X=lambda S:(min(A for A,B in S),max(A for A,B in S),min(B for A,B in S),max(B for A,B in S))
	L=0;Y=0,0,0,0
	for I,Z in C.items():
		a,b,c,d=X(Z)
		if(b-a+1)*(d-c+1)==len(Z):L=I;Y=a,b,c,d;break
	if L<1:return g
	M=[A for A in C if A-L][0];e=C[M];N={(A,B)for A,B in e if all(0<=A+i<T and 0<=B+j<U and g[A+i][B+j]==M for i,j in[(-1,-1),(-1,1),(1,-1),(1,1)])}
	if not N:return g
	l,m,n,o=X(N);E,J,D,F=l-1,m+1,n-1,o+1;O=[r[:]for r in g];P,f,K,Q=Y
	for A,B in e:O[A][B]=0
	R=lambda a,b,c,d:b>=c and a<=d;p=R(D,F,K,Q);G=H=0
	if p:G=1if E+J<P+f else-1
	else:H=1if D+F<K+Q else-1
	while not(R(D,F,K,Q)and(P-J==1or E-f==1)or R(E,J,P,f)and(K-F==1or D-Q==1)):E+=G;J+=G;D+=H;F+=H
	for A in range(max(0,E),min(T,J+1)):
		for B in range(max(0,D),min(U,F+1)):O[A][B]=M
	return O
