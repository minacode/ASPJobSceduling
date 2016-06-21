operation(pseudo).
starts(pseudo, m0, 0).
lasts(pseudo, 0).

operation(j0o0).
dependson(j0o0, pseudo).
lasts(j0o0, 1).
runson(j0o0, m0).

operation(j0o1).
dependson(j0o1, j0o0).
lasts(j0o1, 1).
runson(j0o1, m0).

machine(m0).

%2{starts(O, M, T) : operation(O), machine(M), T = 1..2}2.
%:- #count {J : starts(J, _, _)} != 2, operation(J).
%:- starts(J1, _, _), starts(J2, _, _), J1 = J2.
2{starts(J, M, T) : dependson(J, A), endsbefore(J, A), runson(J, M), isfree(M, T), operation(J), operation(A), machine(M)}2.
endsbefore(J, A)     :- starts(J, _, Z), endsat(A, T), Z < T, operation(J), operation(A).
isfree(M, T + W + 1) :- starts(J, M, T), lasts(J, W), operation(J), machine(M).
%isfree(M, T + 1)    :- not starts(_ , M, T+1), isfree(M, T).
endsat(J, T + W)     :- starts(J, _, T), lasts(J, W), operation(J).
max(S)               :- S = #max { T : endsat(_, T) }.
%#minimize { V : max(V) }.
%#show starts/3.