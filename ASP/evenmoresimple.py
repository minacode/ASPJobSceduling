import subprocess

class Operation:
    def __init__(self, job, machine, cost, rank):
        self.job        = job
        self.machine    = machine
        self.cost       = cost
        self.rank       = rank
        self.start_time = None

    def get_name(self):
        return 'j' + str(self.job) + 'o' + str(self.rank)
       
    def get_dependency(self):
        return 'j' + str(self.job) + 'o' + str(self.rank -1)
       
    def update_from_term(self, term):
        # remove ')'
        term = term[:-1]

        # split by whitespace 
        term_values = term.split(',')
 
        # set start time
        self.start_time = term_values[1] 

 
def get_time_intervall(rank, job_count):
    return str(rank * job_count) + '..' + str(((rank +2) * job_count) -1)
     
def parse_solver_output(output, operations):
    # split lines
    solver_lines = output.splitlines()
    
    # delete all unnecessary lines from beginning
    while solver_lines[0] != 'Solving...':
        del solver_lines[0]

    # terminate if unsatisfiable
    if solver_lines[1] == 'UNSATISFIABLE':
        return None
        
    # delete satisfiability-information
    del solver_lines[0]
    
    # keep all solutions
    i = 0
    while solver_lines[i] != 'OPTIMUM FOUND':
        i += 1
    
    # delete lines after solutions
    for j in range(len(solver_lines) - i):
        del solver_lines[i]
    
    # take terms of last solution
    solution_terms = solver_lines[-2].split()
    
    # this works, because python can do some great sort-magic with strings
    # it's sorted charwise by alphabetical and numerical order
    # thus, j0o0 < j0o1 and j0o0 < j1o0
    # pseudo is the last element
    solution_terms.sort()
    
    # delete pseudo, because it has no operation-representation
    del solution_terms[-1]
    
    for i in range(len(operations)):
        operations[i].update_from_term(solution_terms[i]) 
    
    return operations 
     
     
output_file_name = 'evenmoresimplersolution.lp'
file_name = input('file: ')
with open(file_name + '.txt', 'r') as file:
    lines = file.readlines()
    counts = lines[0].split()
    machine_count = int(counts[0])
    job_count = int(counts[1])
    operation_count = machine_count * job_count
    del lines[0]
    operations = []
    max_operation_count = 0
    
    for i in range(len(lines)):
        line = lines[i].split()
        op_count = len(line) // 2
        if op_count > max_operation_count:
            max_operation_count = op_count
        for j in range(0, len(line), 2):
            print('creating operation : ', i, line[j], line[j+1], j // 2)
            operations.append(Operation(job = i, machine = 'm' + line[j], cost = line[j+1], rank = j // 2))

with open(output_file_name, 'w') as f:
    f.write('runson(pseudo, m0).\n'
            'starts(pseudo, -1).\n\n')
    
    operation_counts = [0] * max_operation_count
    for operation in operations:
        operation_counts[operation.rank] += 1
        f.write('operation' + str(operation.rank) + '(' + operation.get_name() + ').\n')
        if operation.rank == 0:
            f.write('dependson(' + operation.get_name() + ', pseudo).\n')
        else:
            f.write('dependson(' + operation.get_name() + ', ' + operation.get_dependency() + ').\n')
        f.write('runson(' + operation.get_name() + ', ' + operation.machine + ').\n\n')
    
    for i in range(len(operation_counts)):
        f.write('' + str(operation_counts[i]) + ''
                '{starts(J, T) : operation' + str(i) + '(J), T = ' + get_time_intervall(i, job_count) + '}'
                '' + str(operation_counts[i]) + '.\n'
               )
    
    f.write(':- dependson(J, A), starts(J, T), starts(A, Z), T <= Z.\n'
            ':- starts(J, T), starts(A, Z), runson(J, M), runson(A, M), T = Z, J != A.\n'
            ':- starts(J, T), starts(J, Z), Z != T.\n'
            'max(S + 1) :- S = #max { T : starts(_, T)}.\n'
            '#minimize { T : max(T) }.\n'
            '#show starts/2.'
           )

# create subprocess definition
process = ['clingo', output_file_name, '--solve-limit=100000', '-n 10', '-t 4']

# run subprocess, not sure, if busy-waiting..
completed_process = subprocess.run(process, universal_newlines = True, stdout = subprocess.PIPE, stderr = subprocess.DEVNULL)

# update operations based on solver output
operations = parse_solver_output(completed_process.stdout, operations)

# this is not the real starting time, but the intervall in which it starts
for operation in operations:
    print(operation.start_time)

# TODO: we need to calculate real times based on costs of the operations
