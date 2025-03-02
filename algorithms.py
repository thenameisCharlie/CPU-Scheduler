from collections import deque
from operator import itemgetter
from tabulate import tabulate

# Function to print completed processes
def print_completed_processes(complete):
    print("Completed Processes:", end=' ')
    for process, val in complete.items():
        if val == 1:
            print(process, end=' ')
    print()

# Function to print queue state
def print_queue(q, processes, process_burst_index):
    print(f"{'Process':<10}{'Burst':<10}")
    if q:
        for pid in list(q):
            print(f"{pid:<9}{processes[pid][process_burst_index[pid]]:<10}")
    else:
        print(f"{'empty':<10} {'empty':<10}")
    print()

# Function to print context switch details
def print_context_switch(processes, process_index, ready_queue, process_burst_index, time):
    print(f"Current Execution Time: {time}\n")
    print(f"Next Process on the CPU: {process_index}")
    print("Ready queue:")
    print_queue(ready_queue, processes, process_burst_index)

# First Come First Serve (FCFS) Algorithm
def fcfs_scheduling(processes):
    ready_queue = deque(processes.keys())
    process_burst_index = {p: 0 for p in processes}
    io_return = [(float('inf'), p) for p in processes]
    arrival_time = {p: 0 for p in processes}
    waiting_time = {p: 0 for p in processes}
    tat = {p: 0 for p in processes}
    response_time = {p: -1 for p in processes}
    complete = {p: 0 for p in processes}
    time = 0
    idle_cpu_time = 0
    
    while ready_queue:
        process_index = ready_queue.popleft()
        waiting_time[process_index] += time - arrival_time[process_index]
        
        if response_time[process_index] == -1:
            response_time[process_index] = time - arrival_time[process_index]
        
        print_context_switch(processes, process_index, ready_queue, process_burst_index, time)
        time += processes[process_index][process_burst_index[process_index]]
        
        if process_burst_index[process_index] <= len(processes[process_index]) - 3:
            for i, (ret_time, idx) in enumerate(io_return):
                if idx == process_index:
                    io_return[i] = (processes[process_index][process_burst_index[process_index] + 1] + time, idx)
                    break
        else:
            complete[process_index] = 1
        
        print_completed_processes(complete)
        process_burst_index[process_index] += 2
        io_return.sort(key=itemgetter(0))
        
        if not ready_queue:
            while io_return[0][0] != float('inf') and io_return[0][0] > time:
                time += 1
                idle_cpu_time += 1
        
        for i, (ret_time, idx) in enumerate(io_return):
            if ret_time <= time:
                ready_queue.append(idx)
                arrival_time[idx] = ret_time
                io_return[i] = (float('inf'), idx)
    
    burst_time = time - idle_cpu_time
    
    for p in processes:
        tat[p] = sum(processes[p]) + waiting_time[p]
    
    avg_waiting_time = sum(waiting_time.values()) / len(processes)
    avg_turnaround_time = sum(tat.values()) / len(processes)
    avg_response_time = sum(response_time.values()) / len(processes)
    cpu_utilization = burst_time / time * 100
    
    results_table = [
        ["Metric", "Value"],
        ["Total Time", time],
        ["CPU Utilization", f"{cpu_utilization:.2f}%"],
        ["Avg Waiting Time", f"{avg_waiting_time:.2f}"],
        ["Avg Turnaround Time", f"{avg_turnaround_time:.2f}"],
        ["Avg Response Time", f"{avg_response_time:.2f}"]
    ]
    print(tabulate(results_table, headers="firstrow", tablefmt="grid"))

#SJF Algorithm
def sjf_scheduling(processes):
    print("SJF Algorithm not yet implemented.")

# User input to choose algorithm
algorithmSelection = input("Please choose an algorithm to run:\n1. First Come First Serve (FCFS)\n2. Shortest Job First (SJF)\n3. Multilevel Feedback Queue Scheduling (MLFQ)\n")

if algorithmSelection == "1":
    processes = {"p1":[5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4],
                "p2":[4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8],
                "p3":[8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6],
                "p4":[3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3],
                "p5":[16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4],
                "p6":[11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8],
                "p7":[14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10],
                "p8":[4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]}
    
    fcfs_scheduling(processes)

elif algorithmSelection == "2":
    print("SJF Algorithm not yet implemented.")


elif algorithmSelection == "3":
    print("MLFQ Algorithm not yet implemented.")

else:
    print("Invalid selection. Please restart the program.")