from collections import deque,Counter
def p(i):
 T=lambda a:Counter([B for A in a for B in A]if isinstance(a,list)and a and isinstance(a[0],list)else[A for(A,B)in a]).most_common(1)[0][0]if a else 0
 def a(G):
  E,F=len(G),len(G[0]);K=T(G);D=[[0]*F for _ in range(E)];j=[]
  for c in range(E):
   for d in range(F):
    L=deque([(c,d)]);M=[]
    while L:
     A,B=L.popleft()
     if not(0<=A<E and 0<=B<F)or D[A][B]:continue
     C=G[A][B]
     if C==K:continue
     D[A][B]=1;M.append((C,(A,B)))
     for(J,C)in[(A+P,B+Q)for P in(-1,0,1)for Q in(-1,0,1)if P or Q]:L.append((J,C))
    if M:j.append(M)
  return j
 A=lambda d:(min(A for(A,B)in d),min(A for(B,A)in d),max(A for(A,B)in d),max(A for(B,A)in d));U=lambda d:(A(d)[0]+(A(d)[2]-A(d)[0])//2,A(d)[1]+(A(d)[3]-A(d)[1])//2)
 h=lambda a,b:((lambda P,Q,R,S:(0if P==R else 1if P<R else-1,1if Q<S else-1))(*U(a),*U(b)))
 l=lambda a,X:[(B,(X[0]+X[2]-C,D))for(B,(C,D))in a];W=lambda a,X:[(B,(C,X[1]+X[3]-D))for(B,(C,D))in a];D=lambda a,o:[(A,(B+o[0],C+o[1]))for(A,(B,C))in a]
 L=lambda G,C:[[next((B for(B,(D,E))in C if D==r and E==c and B),G[r][c])for c in range(len(G[0]))]for r in range(len(G))]
 M=lambda G,d:next((G[A][B]for(A,B)in d if G[A][B]),0)
 y=a(i);C=[A[:]for A in i];j,I=[],[]
 for B in y:
  E=T(B);Y=[A for A in B if A[0]==E];m=[A for A in B if A[0]!=E];e=[A for(B,A)in Y];G=[A for(B,A)in m];c=Y[0];n=G+[c[1]]if G else[c[1]];V=A(n);r={(A,B)for A in range(V[0],V[2]+1)for B in range(V[1],V[3]+1)};J,K=h(e,G if G else e);X=A([A for(B,A)in B]);H,w=X[2]-X[0]+1,X[3]-X[1]+1;F=lambda p:-p and(1-p if p<0else-1-p);s,t,o=(H*J,0),(0,w*K),(H*J,w*K);u,v,x=(F(J),0),(0,F(K)),(F(J),F(K));Z=[A for(B,A)in B];m=[A for A in D(l(B,X),s)if A[0]==E];e=[A for A in D(W(B,X),t)if A[0]==E];z=[A for A in D(l(W(B,X),X),o)if A[0]==E];b,c,q=D(m,u),D(e,v),D(z,x);j+=[(M(i,{A for(B,A)in b if A in r}),A)for(B,A)in b];I+=[(M(i,{A for(B,A)in c if A in r}),A)for(B,A)in c]+[(M(i,{A for(B,A)in q if A in r}),A)for(B,A)in q]
 return L(L(C,j),I)
