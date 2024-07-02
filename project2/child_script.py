# Group No: 24
# Bilge Kaan Güneyli 2020400051
# Ömer Faruk Erzurumluoğlu 2021400336

import sys
from mpi4py import MPI
import math

parent_comm = MPI.Comm.Get_parent()
comm = MPI.COMM_WORLD
machine_no = comm.Get_rank() + 1


def add(str1, str2):
    return str1 + str2


def enhance(str):
    ret = str[0] + str + str[len(str) - 1]
    return ret


def reverse(str):
    return str[::-1]


def chop(str):
    if (len(str) < 2):
        return str
    return str[:len(str) - 1]


def trim(str):
    if (len(str) < 3):
        return str
    return str[1:len(str) - 1]


def split(str):
    cut = math.ceil(len(str) / 2)
    return str[:cut]

# read the input and create the variables
input = sys.argv[1].split("\n")
nof_production_cycles = int(input[0])
wf = [int(item) for item in input[1].split()]   # put the wear factors in a list
threshold = int(input[2])

my_childs_rank     =  []      # will hold the rank of process this process has to wait
leaf_input_strings =  []      # will hold the inputs for leaf nodes
all_nodes          =  set()   # will hold the machine numbers for all nodes
non_leaf_nodes     =  set()   # will hold the machine numbers for non-leaf nodes
current_wear       =  0       # will hold the wear of the machine
my_parent_rank     = -1       # will hold the machine number of the process which we have to send message to
maintenance_count  =  0       # will hold the number of maintenances this machine has been through
last_request       =  0       # will help us the ensure synchronization of messages

for i in range(3, len(input)):
    line = input[i].split()

    if len(line) > 1:
        parent_no = int(line[1])
        current_no = int(line[0])
        all_nodes.add(current_no)
        non_leaf_nodes.add(parent_no)

        if parent_no == machine_no:  # if this process is parent of any other process
            my_childs_rank.append(current_no - 1)
            continue
        elif current_no == machine_no:  # if the current process is this process
            my_parent_rank = parent_no - 1
            next_state = line[2]  # the state which we will enter the FSM from

    else:   # the lines that contain the inputs for leaf nodes
        leaf_input_strings.append(line[0])  

my_childs_rank.sort()
leaf_nodes = list(all_nodes.difference(non_leaf_nodes))
leaf_nodes.sort()


for cpc in range(nof_production_cycles):   

    if len(my_childs_rank) > 0:  # if this machine is a parent of some machine
        resource = ""
        for child_rank in my_childs_rank:
            resource = add(resource, comm.recv(source=child_rank, tag=0))   # add the inputs that you get

    else:   # if this machine is a leaf machine take the input from the list
        for i in range(len(leaf_nodes)):
            if leaf_nodes[i] == machine_no:
                resource = leaf_input_strings[i]


    if machine_no == 1:   # if you are the machine 1, send your added input to the control room
        output = resource
        if last_request != 0:   # wait until the previous message is read
            last_request.wait()
        parent_comm.isend(output, dest=0, tag=0)

    else:   # go into the FSM
        state = next_state
        if state == "split":   # employ wear, create output, apply maintenance process if necessary
            current_wear += wf[4]
            output = split(resource)
            next_state = "chop"
            cost = (current_wear - threshold + 1) * wf[4]
            if cost >= wf[4]:
                message = str(machine_no) + "-" + str(cost) + "-" + str(cpc + 1)
                if last_request != 0:
                    last_request.wait()
                last_request = parent_comm.isend(message, dest=0, tag=1)
                current_wear = 0
                maintenance_count += 1

        elif state == "chop":
            current_wear += wf[2]
            output = chop(resource)
            next_state = "enhance"
            cost = (current_wear - threshold + 1) * wf[2]
            if cost >= wf[2]:
                message = str(machine_no) + "-" + str(cost) + "-" + str(cpc + 1)
                if last_request != 0:
                    last_request.wait()
                last_request = parent_comm.isend(message, dest=0, tag=1)
                current_wear = 0
                maintenance_count += 1

        elif state == "enhance":
            current_wear += wf[0]
            output = enhance(resource)
            next_state = "split"
            cost = (current_wear - threshold + 1) * wf[0]
            if cost >= wf[0]:
                message = str(machine_no) + "-" + str(cost) + "-" + str(cpc + 1)
                if last_request != 0:
                    last_request.wait()
                last_request = parent_comm.isend(message, dest=0, tag=1)  
                current_wear = 0
                maintenance_count += 1


        elif state == "reverse":
            current_wear += wf[1]
            output = reverse(resource)
            next_state = "trim"
            cost = (current_wear - threshold + 1) * wf[1]
            if cost >= wf[1]:
                message = str(machine_no) + "-" + str(cost) + "-" + str(cpc + 1)
                if last_request != 0:
                    last_request.wait()
                last_request = parent_comm.isend(message, dest=0, tag=1)  
                current_wear = 0
                maintenance_count += 1

        elif state == "trim":
            current_wear += wf[3]
            output = trim(resource)
            next_state = "reverse"
            cost = (current_wear - threshold + 1) * wf[3]
            if cost >= wf[3]:
                message = str(machine_no) + "-" + str(cost) + "-" + str(cpc + 1)
                if last_request != 0:
                    last_request.wait()
                last_request = parent_comm.isend(message, dest=0, tag=1) 
                current_wear = 0
                maintenance_count += 1

        if last_request != 0:
            last_request.wait()
        comm.send(output, dest=my_parent_rank, tag=0)   # send the output to parent

if last_request != 0:
    last_request.wait()

parent_comm.isend(maintenance_count, dest=0, tag=2)   # send the number of maintenances to the control room

MPI.Finalize()