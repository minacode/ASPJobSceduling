runson(pseudo, m0).
starts(pseudo, -1).

operation0(j0o0).
dependson(j0o0, pseudo).
runson(j0o0, m0).

operation1(j0o1).
dependson(j0o1, j0o0).
runson(j0o1, m1).

operation2(j0o2).
dependson(j0o2, j0o1).
runson(j0o2, m2).

operation0(j1o0).
dependson(j1o0, pseudo).
runson(j1o0, m2).

operation1(j1o1).
dependson(j1o1, j1o0).
runson(j1o1, m1).

operation2(j1o2).
dependson(j1o2, j1o1).
runson(j1o2, m0).

operation0(j2o0).
dependson(j2o0, pseudo).
runson(j2o0, m0).

operation1(j2o1).
dependson(j2o1, j2o0).
runson(j2o1, m2).

operation2(j2o2).
dependson(j2o2, j2o1).
runson(j2o2, m1).

3{starts(J, T) : operation0(J), T = 0..5}3.
3{starts(J, T) : operation1(J), T = 3..8}3.
3{starts(J, T) : operation2(J), T = 6..11}3.
:- dependson(J, A), starts(J, T), starts(A, Z), T <= Z.
:- starts(J, T), starts(A, Z), runson(J, M), runson(A, M), T = Z, J != A.
:- starts(J, T), starts(J, Z), Z != T.
max(S + 1) :- S = #max { T : starts(_, T)}.
#minimize { T : max(T) }.
#show starts/2.