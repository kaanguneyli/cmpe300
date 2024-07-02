# Bilge Kaan Guneyli 2020400051
# Omer Faruk Erzurumluoglu 2021400336

import random
import math
import time

from tabulate import tabulate
import os
import sys

_location_ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(_file_)))
noftrials = 100000


def move(liste: list, current: tuple):  # does a random move from given table & current position of the knight
    doable = []
    for next_move in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2),
                      (-1, -2)]:  # check all possible moves
        if -1 < current[0] + next_move[0] < 8 and -1 < current[1] + next_move[1] < 8 and \
                liste[current[0] + next_move[0]][current[1] + next_move[1]] == -1:
            doable.append((current[0] + next_move[0], current[1] + next_move[1]))
    if len(doable) == 0:  # if no possible moves, return
        next = (-1, -1)
        return next
    # add a new random movement to the table
    maximuz = max([max(i) for i in liste])
    next = doable[random.randint(0, len(doable) - 1)]
    new_liste = [i.copy() for i in liste]
    new_liste[next[0]][next[1]] = maximuz + 1
    return new_liste, next


if sys.argv[1] == "part1":
    # time_file = open(os.path.join(_location, r"results" + "part1" + ".txt"), 'w+')
    # start running Las Vegas Algorithm for various p
    for p in [0.7, 0.8, 0.85]:
        file = open(os.path.join(_location, r"results" + str(p) + ".txt"), 'w+')
        success = 0
        start_time = time.time()
        # try 100000 times
        for run in range(noftrials):
            starting_table = [[-1 for _ in range(8)] for _ in range(8)]
            start = (random.randint(0, 7), random.randint(0, 7))
            starting_table[start[0]][start[1]] = 0
            file.write(f"Run {run + 1}: starting from ({start[0]},{start[1]})\n")
            next_table, start = move(starting_table, start)
            current_table = starting_table
            # until we meet a dead end we move
            while next_table != -1:
                file.write(f"Stepping to ({start[0]},{start[1]})\n")
                current_table = next_table
                next_table, start = move(next_table, start)
            maximuz = max([max(i) for i in current_table])
            maximuz += 1
            # check if the result holds our expectations
            if maximuz >= math.ceil(64 * p):
                file.write(f"Successful - Tour length: {maximuz}\n")
                success += 1
            else:
                file.write(f"Unsuccessful - Tour length: {maximuz}\n")
            file.write(tabulate(current_table, tablefmt="plain") + "\n\n")
        end = time.time()
        # time_file.write(f"p = {p}: {end-start_time}\n")
        file.close()
        print(
            f"LasVegas Algorithm With p = {p}\nNumber of successful tours : {success}\nNumber of trials : {noftrials}\nProbability of a successful tour : {success / noftrials}\n")
    # time_file.close()

elif sys.argv[1] == "part2":
    # time_file = open(os.path.join(_location, r"results" + "part2" + ".txt"), 'w+')
    # start running Las Vegas Algorithm with backtracking for various p
    for p in [0.7, 0.8, 0.85]:
        print(f"--- p = {p} ---")
        # start with k times of random movements
        for k in [0, 2, 3]:
            success = 0
            start_time = time.time()
            # try 100000 times
            for _ in range(noftrials):
                starting_table = [[-1 for _ in range(8)] for _ in range(8)]
                start = (random.randint(0, 7), random.randint(0, 7))
                starting_table[start[0]][start[1]] = 0
                # do k random moves
                for _ in range(k):
                    starting_table, start = move(starting_table, start)
                table_stack = [(starting_table, start, k + 1)]
                # try to find a table which knight has moved sufficiently & which starts with the given random start (DFS)
                while len(table_stack) > 0:
                    current_table, current, tour_length = table_stack.pop()
                    if tour_length >= 64 * p:
                        success += 1
                        # print(tabulate(current_table))
                        break
                    # find all of the moves & add all of the possible tables to the a stack
                    for next_move in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                        if -1 < current[0] + next_move[0] < 8 and -1 < current[1] + next_move[1] < 8 and \
                                current_table[current[0] + next_move[0]][current[1] + next_move[1]] == -1:
                            new_liste = [i.copy() for i in current_table]
                            new_liste[current[0] + next_move[0]][current[1] + next_move[1]] = tour_length
                            table_stack.append(
                                (new_liste, (current[0] + next_move[0], current[1] + next_move[1]), tour_length + 1))
            print(
                f"LasVegas Algorithm With p = {p} , k = {k}\nNumber of successful tours : {success}\nNumber of trials : {noftrials}\nProbability of a successful tour : {success / noftrials}\n")
            end = time.time()
            # time_file.write(f"p = {p}, k = {k}: {end-start_time}\n")
    # time_file.close()