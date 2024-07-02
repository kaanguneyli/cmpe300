# Group No: 24
# Bilge Kaan Güneyli 2020400051
# Ömer Faruk Erzurumluoğlu 2021400336

import sys
import math
from mpi4py import MPI

with open(sys.argv[1], 'r') as file:
    num_processes = int(file.readline().strip())   # the number of processes
    file_contents = file.read()

intercomm = MPI.COMM_SELF.Spawn(   # spawn childs 
    sys.executable,
    args = ['child_script.py', file_contents],   # send the rest of the text in the file to the children
    maxprocs = num_processes
)

production_cycles = int(file_contents.split("\n")[0])   # read the number of production cycles
product_no = 0
with open(sys.argv[2], 'w') as file:   # open the file in write format to clear the content inside
    pass

maintenance_logs = []   
for _ in range(num_processes):
    maintenance_logs.append([])   # this 2-d list will hold the log related to maintenance

maintenance_count = num_processes   # this variable will help us to be sure that we take all the maintenance info from children
maintenance_limit = 0    # this variable will be equal to total number of maintenances

status = MPI.Status()
while (product_no < production_cycles or status.tag != -1 or maintenance_limit != 0 or maintenance_count != 0):   # work until the processes are completed and maintenances are taken
    if intercomm.iprobe(source=status.source, tag=status.tag, status=status):   # check did we receive any message
        if status.tag == 0:   # new product message
            output = intercomm.recv(source=status.source, tag=0, status=status)
            with open(sys.argv[2], 'a') as file:
                file.write(output + "\n")
            product_no += 1

        elif status.tag == 1:   # maintenance message
            received = intercomm.recv(source=status.source, tag=1, status=status)
            maintenance_logs[status.source].append(received + "\n")   # store the message in a list to be able to write to file in correct order at the end
            maintenance_limit -= 1   # reduce because we are sure that one maintenance is received

        elif status.tag == 2:   # number of maintenances which is send at the end of process by each child
            maintenance_limit += intercomm.recv(source=status.source, tag=2, status=status)
            maintenance_count -= 1   # reduce because we are sure one child is done with sending maintenance messages

    status = MPI.Status()

# create the maintenance log string
logs = ""
for machine in maintenance_logs:
    for log in machine:
        logs += log

with open(sys.argv[2], 'a') as file:
    file.write(logs)