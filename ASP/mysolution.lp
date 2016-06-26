operation(pseudo).
lasts(pseudo, 0).
runson(pseudo, m0).
starts(pseudo, 0).

operation(j0o0).
dependson(j0o0, pseudo).
lasts(j0o0, 1).
runson(j0o0, m0).

operation(j0o1).
dependson(j0o1, j0o0).
lasts(j0o1, 1).
runson(j0o1, m0).

machine(m0).

3{starts(J, T) : operation(J), isstarttime(T)}3.
:- dependson(J, A), starts(J, T), endsat(A, Z), Z >= T.
:- starts(J, TA), endsat(J, TE), runson(J, M), runson(A, M), endsat(A, ZE), TA <= ZE, ZE <= TE, J != A.
:- starts(J, T), starts(J, Z), Z != T.
endsat(J, T + W - 1) :- starts(J, T), lasts(J, W).
isstarttime(T + 1) :- endsat(_, T), T < 2.
max(S) :- S = #max { T : endsat(_, T) }.
#minimize { V : max(V) }.
#show starts/2.