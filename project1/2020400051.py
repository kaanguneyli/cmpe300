from random import randint
from timeit import default_timer as timer
import math

def algorithm(arr):
    start = timer()
    y = 0
    n = len(arr)
    for i in range(0,n):
        if arr[i] == 0:
            for j in range(i,n):
                y += 1
                k = n
                while k > 0:
                    k //= 3
                    y += 1
        elif arr[i] == 1:
            for m in range(i,n):
                y += 1
                for l in range(m,n):
                    for t in range(n,0,-1):
                        for z in range(n,0,-t):
                            y += 1
        else:
            y += 1
            p = 0
            while p < n:
                for j in range(0, p**2 - 1):
                    y += 1
                p += 1
    end = timer()
    time = end - start
    return time

def omer_func(x):
    res = 0
    for t in range(1,x+1):
        res += math.floor(x/t)
    return res

n_list = [1,5,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]
best_case_time_list = []
worst_case_time_list = []
avg_case_time_list = []

for n in n_list:
    best_arr=[]
    worst_arr=[]

    average_case_times=[]
        
    thres_root_up = n*(n-1)*(2*n-1)
    thres_root_down = 3*(omer_func(n-1)+n)
    thres_root = (thres_root_up/thres_root_down+0.25)**0.5
    threshold = math.ceil(n+0.5-thres_root) -1                 # calculate the treshold when the item to create the worst case changes from 1 to 2
    for a in range(n):
        best_arr.append(0)     # best case consists only 0's
        if a < threshold:
            worst_arr.append(1)
        else:
            worst_arr.append(2)
    
    best_case_time = algorithm(best_arr)
    worst_case_time = algorithm(worst_arr)
        
    best_case_time_list.append(best_case_time)        #GRAFİK SONRASI GEREKSİZ
    worst_case_time_list.append(worst_case_time)      #GRAFİK SONRASI GEREKSİZ
        
    for b in range(12):  # execute 12 different average cases
        average_arr=[]
        for c in range(n):
            average_arr.append(randint(0,2))  # creating the average case input with a random generator
        average_case_times.append(algorithm(average_arr))
    avg_case_time_list.append(average_case_times)     #GRAFİK SONRASI GEREKSİZ
        

    print('Case: best Size:', n, 'Elapsed Time (s):', best_case_time)
    print('Case: worst Size:', n, 'Elapsed Time (s):', worst_case_time)
    print('Case: average Size:', n, 'Elapsed Time (s):', ' '.join(map(str, average_case_times)))


