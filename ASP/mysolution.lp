operation(pseudo).
lasts(pseudo, 0).
runson(pseudo, m0).
starts(pseudo, m0, 0).

operation(j0o0).
dependson(j0o0, pseudo).
lasts(j0o0, 4).
runson(j0o0, m0).

operation(j0o1).
dependson(j0o1, j0o0).
lasts(j0o1, 3).
runson(j0o1, m1).

operation(j0o2).
dependson(j0o2, j0o1).
lasts(j0o2, 5).
runson(j0o2, m2).

operation(j1o0).
dependson(j1o0, pseudo).
lasts(j1o0, 6).
runson(j1o0, m2).

operation(j1o1).
dependson(j1o1, j1o0).
lasts(j1o1, 3).
runson(j1o1, m1).

operation(j1o2).
dependson(j1o2, j1o1).
lasts(j1o2, 4).
runson(j1o2, m0).

operation(j2o0).
dependson(j2o0, pseudo).
lasts(j2o0, 6).
runson(j2o0, m0).

operation(j2o1).
dependson(j2o1, j2o0).
lasts(j2o1, 3).
runson(j2o1, m2).

operation(j2o2).
dependson(j2o2, j2o1).
lasts(j2o2, 3).
runson(j2o2, m1).

machine(m0).
machine(m1).
machine(m2).

10{starts(J, M, T) : runson(J, M), operation(J), isstarttime(T), machine(M)}10.
:- dependson(J, A), starts(J, _, T), endsat(A, Z), Z >= T.
:- starts(J, M, TA), endsat(J, TE), runson(A, M), endsat(A, ZE), TA <= ZE, ZE <= TE, J != A.
:- starts(J, _, T), starts(J, _, Z), Z != T.
endsat(J, T + W - 1) :- starts(J, _, T), lasts(J, W).
isstarttime(T + 1) :- endsat(_, T), T < 37.
max(S) :- S = #max { T : endsat(_, T) }.
#minimize { V : max(V) }.
%#show starts/3.
#show isstarttime/1.
