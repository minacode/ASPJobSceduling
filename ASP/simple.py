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
job_count = int(counts[0])
operation_count = machine_count * job_count
del lines[0]
operations = []
machines = []
for i in range(machine_count):
    machines.append("m"+ str(i))
    a = lines[i].split()
    for j in range(0, len(a), 2):
        operations.append(Operation(job = i, machine = 'm' + a[j], cost = a[j+1], rank = j // 2))
file.close()

f = open('easysolution.lp', 'w')

f.write('operation(pseudo).\n'
        'runson(pseudo, m0).\n'
        'starts(pseudo, 0).\n\n')

for operation in operations:
    f.write('operation(' + operation.get_name() + ').\n')
    if operation.rank == 0:
        f.write('dependson(' + operation.get_name() + ', pseudo).\n')
    else:
        f.write('dependson(' + operation.get_name() + ', ' + operation.get_dependency() + ').\n')
    f.write('runson(' + operation.get_name() + ', ' + operation.machine + ').\n\n')
        
for machine in machines:
    f.write('machine(' + machine + ').\n')
f.write('\n')

f.write('' + str(operation_count + 1) + '' 
        '{starts(J, T) : operation(J), T = 0..' + str(machine_count * 4) + '}' + str(operation_count + 1) + '.\n'
        ':- dependson(J, A), starts(J, T), starts(A, Z), T <= Z.\n'
        ':- starts(J, T), starts(A, Z), runson(J, M), runson(A, M), T = Z, J != A.\n'
        ':- starts(J, T), starts(J, Z), Z != T.\n'
        'max(S + 1) :- S = #max { T : starts(_, T)}.\n'
        '#minimize { T : max(T) }.\n'
        '#show starts/2.'
       )

f.close()

os.system('clingo easysolution.lp --solve-limit=100000 -n 10 -t 3')
