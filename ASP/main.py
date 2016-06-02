import os

class Operation:
    def __init__(self, job, machine, cost, rank):
        self.job     = job
        self.machine = machine
        self.cost    = cost
        self.rank    = rank

    def get_name(self):
        return 'j' + str(self.job) + 'o' + str(self.rank)
       
    def get_dependency(self):
        return 'j' + str(self.job) + 'o' + str(self.rank -1)
        

file = open('1.txt', 'r')
lines = file.readlines()
counts = lines[0].split()
del lines[0]
operations = []
for i in range(len(lines)):
    a = lines[i].split()
    for j in range(0, len(a), 2):
        operations.append(Operation(job = i, machine = a[j], cost = a[j+1], rank = j // 2))
file.close()

f = open('mysolution.lp', 'w')
for operation in operations:
    if operation.rank == 0:
        f.write('dependson(' + operation.get_name() + ', pseudo).\n')
    else:
        f.write('dependson(' + operation.get_name() + ', ' + operation.get_dependency() + ').\n')
    f.write('lasts(' + operation.get_name() + ', ' + operation.cost + ').\n')
    f.write('runson(' + operation.get_name() + ', ' + operation.machine + ').\n')
        
f.write('starts(pseudo, 0, 0).\n lasts(pseudo, 0).\n')
f.write('starts(J, M, T)  :- dependson(J, A), endsbefore(A, T), runson(J, M), isfree(M, T).\n'
        'endsbefore(J, T) :- starts(J, _, Z), Z + W < T, lasts(J, W).\n'
        'isfree(M, T)     :- starts(J, M, Z), Z < T, lasts(J, W), Z + W <= T.\n'
        'endsat(J, T)     :- T = #sum { Z, W : starts(J, _, Z), lasts(J, W) }.\n'
        'max(X)           :- X = #max { T : endsat(J, T) }.\n'
        '#minimize { X : max(X) }.\n'
       )
f.close()


os.system('clingo 0 mysolution.lp')
