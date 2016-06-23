operation(pseudo).
lasts(pseudo, 0).
runson(pseudo, m0).
starts(pseudo, m0, 0).

operation(j0o0).
dependson(j0o0, pseudo).
lasts(j0o0, 1).
runson(j0o0, m0).

operation(j0o1).
dependson(j0o1, j0o0).
lasts(j0o1, 1).
runson(j0o1, m0).

machine(m0).

1{starts(J, M, T) : dependson(J, A), endsat(A, Z), Z < T, runson(J, M), not collide(J, A), operation(J), operation(A), isstarttime(T), machine(M)}.
collide(J, A) :- starts(J, M, TA), endsat(J, TE), runson(A, M), endsat(A, ZE), TA <= ZE, ZE <= TE.
endsat(J, T + W - 1) :- starts(J, _, T), lasts(J, W).
isstarttime(T + 1) :- endsat(_, T), T < 2.
max(S) :- S = #max { T : endsat(_, T) }.
#minimize { V : max(V) }.
