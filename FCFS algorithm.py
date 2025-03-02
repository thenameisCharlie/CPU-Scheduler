from collections import deque
from operator import itemgetter
from tabulate import tabulate

# Function to print the completed processes
def print_completed_processes(complete):
    print("Complete Processes: ", end='')
    for i, val in enumerate(complete):
        if val == 1:
            print(f"P{i} ", end='')

# Function to print the current state of the queue
def print_queue(q, processes, process_burst_index):
    print(f"{'Process':<10}{'Burst':<10}")
    if q:
        for pid in list(q):

            print(f"P{pid:<9}{processes[pid][process_burst_index[pid]]:<10}")
    else:
        print(f"{'empty': <10} {'empty': <10}")
    print()

# Function to print the context switch data
def print_context_switch(processes, process_index, ready_queue,process_burst_index, time):
    print(f"Current Execution Time: {time}\n")
    print(f"Next Process on the CPU: P{process_index}")
    print("Ready queue:")
    print_queue(ready_queue, processes, process_burst_index)

# Function for First Come First Serve (FCFS) scheduling algorithm
def fcfs_scheduling(processes, ready_queue, process_burst_index):
 # Initializing necessary variables and lists
    io_return = [(float('inf'), i) for i in range(len(processes))]
    arrival_time = [0] * len(processes)
    waiting_time = [0] * len(processes)
    tat = [0] * len(processes)
    response_time = [-1] * len(processes)
    complete = [0] * len(processes)

    time = 0
    idle_cpu_time = 0

# Loop until there are processes in the ready queue
    while ready_queue:
        # Retrieve the next process from the ready queue
        process_index = ready_queue.popleft()
        # Update waiting time for the current process
        waiting_time[process_index] += time - arrival_time[process_index]

        # Update response time if it's the first time the process is being executed
        if response_time[process_index] == -1:
            response_time[process_index] = time - arrival_time[process_index]

        # Print the context switch data
        print_context_switch(processes, process_index, ready_queue,process_burst_index, time)
 
        # Increment the time by the burst time of the current process
        time += processes[process_index][process_burst_index[process_index]]
 
        # Update the IO return time for the current process if it's not the last burst
        if process_burst_index[process_index] <= len(processes[process_index]) - 3:
                for i, (ret_time, idx) in enumerate(io_return):
                    if idx == process_index:
                        io_return[i] = (processes[process_index][process_burst_index[process_index] + 1] + time,idx)
                        break
        else:
            complete[process_index] = 1
        # Print the completed processes
        print_completed_processes(complete)
        process_burst_index[process_index] += 2
        # Sort the IO return list by time
        io_return.sort(key=itemgetter(0))

        # If the ready queue is empty, simulate idle CPU time until the next process arrives
        if not ready_queue:
            while io_return[0][0] != float('inf') and io_return[0][0] > time:
                time += 1
                idle_cpu_time += 1

        # Add processes to the ready queue if their return time is less than or equal to the current time
        for i, (ret_time, idx) in enumerate(io_return):
            if ret_time <= time:
                ready_queue.append(idx)
                arrival_time[idx] = ret_time
                io_return[i] = (float('inf'), idx)
 
    # Calculate total burst time and print scheduling results
    burst_time = time - idle_cpu_time
    for i, p in enumerate(processes):
        tat[i] += sum(p) + waiting_time[i]
 
    # Printing scheduling results
    print(f"Total time: {len(processes)}")
    print(f"CPU Utilization: {burst_time/time*100:.2f}%\n")
    
    print("Waiting Time")
    total_waiting_time = sum(waiting_time)
    for i, wt in enumerate(waiting_time):
        print(f"Process: {i}, Waiting Time: {wt}")
    print(f"Average Waiting Time: {total_waiting_time/len(processes):.2f}\n")

    print("Turnaround Time")
    total_tat = sum(tat)
    for i, t in enumerate(tat):
        print(f"Process: {i}, Turnaround Time: {t}")
    print(f"Average Turnaround Time: {total_tat/len(processes):.2f}\n")

    print("Response Time")
    total_rt = sum(response_time)
    for i, rt in enumerate(response_time):
        print(f"Process: {i}, Response Time: {rt}")
    print(f"Average Response Time: {total_rt/len(processes):.2f}")

if __name__ == "__main__":
 # Define the processes
    processes = [
    [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4],
    [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8],
    [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6],
     [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3],
    [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4],
    [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8],
    [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10],
    [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]
    ]
    # Initialize the ready queue and process burst index
    ready_queue_fcfs = deque(range(len(processes)))
    process_burst_index = [0] * len(processes)
 
     # Run the FCFS algorithm
    print("FCFS")
    fcfs_scheduling(processes, ready_queue_fcfs, process_burst_index)

