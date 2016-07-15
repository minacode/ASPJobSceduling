runson(pseudo, m0).
starts(pseudo, -1).

operation0(j0o0).
dependson(j0o0, pseudo).
runson(j0o0, m0).

operation1(j0o1).
dependson(j0o1, j0o0).
runson(j0o1, m0).

1{starts(J, T) : operation0(J), T = 0..1}1.
1{starts(J, T) : operation1(J), T = 1..2}1.
:- dependson(J, A), starts(J, T), starts(A, Z), T <= Z.
:- starts(J, T), starts(A, Z), runson(J, M), runson(A, M), T = Z, J != A.
:- starts(J, T), starts(J, Z), Z != T.
max(S + 1) :- S = #max { T : starts(_, T)}.
#minimize { T : max(T) }.
#show starts/2.