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
        
file_name = input('file: ')
file = open(file_name + '.txt', 'r')
lines = file.readlines()
counts = lines[0].split()
machine_count = int(counts[0])
operation_count = int(counts[0])
del lines[0]
operations = []
machines = []
for i in range(machine_count):
    machines.append("m"+ str(i))
    a = lines[i].split()
    for j in range(0, len(a), 2):
        operations.append(Operation(job = i, machine = 'm' + a[j], cost = a[j+1], rank = j // 2))
file.close()

f = open('mysolution.lp', 'w')

f.write('operation(pseudo).\n'
        'lasts(pseudo, 0).\n'
        'runson(pseudo, m0).\n'
        'starts(pseudo, 0).\n\n')

max_sum = 0
for operation in operations:
    max_sum += int(operation.cost)
    f.write('operation(' + operation.get_name() + ').\n')
    if operation.rank == 0:
        f.write('dependson(' + operation.get_name() + ', pseudo).\n')
    else:
        f.write('dependson(' + operation.get_name() + ', ' + operation.get_dependency() + ').\n')
    f.write('lasts(' + operation.get_name() + ', ' + operation.cost + ').\n')
    f.write('runson(' + operation.get_name() + ', ' + operation.machine + ').\n\n')
        
for machine in machines:
    f.write('machine(' + machine + ').\n')
f.write('\n')

f.write('' + str(len(operations) +1 ) + '' 
        '{starts(J, T) : operation(J), isstarttime(T)}' + str(len(operations) +1 ) + '.\n'
        ':- dependson(J, A), starts(J, T), endsat(A, Z), Z >= T.\n'
        ':- starts(J, TA), endsat(J, TE), runson(J, M), runson(A, M), endsat(A, ZE), TA <= ZE, ZE <= TE, J != A.\n'
        ':- starts(J, T), starts(J, Z), Z != T.\n'
        'endsat(J, T + W - 1) :- starts(J, T), lasts(J, W).\n'
        'isstarttime(T + 1) :- endsat(_, T), T < ' + str(max_sum) + '.\n'
        'max(S) :- S = #max { T : endsat(_, T) }.\n'
        '#minimize { V : max(V) }.\n'
        '#show starts/2.'
       )

f.close()

os.system('clingo mysolution.lp')
