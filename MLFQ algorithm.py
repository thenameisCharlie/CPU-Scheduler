from queue import Queue
from collections import deque
from sys import maxsize
# Function to perform Multi-Level Feedback Queue Scheduling
def perform_mlfq(processes, ready_queue_rr1, process_burst_index):
 # Initialize necessary variables and lists
    num_processes = len(processes)
    queue_level = [1] * num_processes
    arrival_time = [0] * len(processes)
    waiting_time = [0] * len(processes)
    tat = [0] * len(processes)
    response_time = [-1] * len(processes)
    ioreturn = [(maxsize, i) for i in range(len(processes))]
    ready_queue_rr2 = deque()
    ready_queue_fcfs3 = deque()
    complete = [0] * num_processes

    # Set all io returns to maximum size
    for i in range(len(processes)):
        ioreturn[i] = (maxsize, i)
    time = 0
    idle_cpu_time = 0
    tqrq1, tqrq2 = 5, 10 # Time quantum values for the different levels of the queue
 
    # Execute until all the queues are empty
    while ready_queue_rr1 or ready_queue_rr2 or ready_queue_fcfs3:
    # Execute processes in the first queue
        if ready_queue_rr1:
            process_index = ready_queue_rr1.popleft()
            # Update waiting time and response time
            waiting_time[process_index] += time - arrival_time[process_index]
            if response_time[process_index] == -1:
                response_time[process_index] = time - arrival_time[process_index]
            local_burst_time = processes[process_index][process_burst_index[process_index]]
            # Print context switch data
            print_context_data(processes, process_index, ready_queue_rr1, process_burst_index, time)
            # Determine the action based on the remaining burst time
            if local_burst_time > tqrq1:
                time += tqrq1

                processes[process_index][process_burst_index[process_index]] = local_burst_time - tqrq1
                ready_queue_rr2.append(process_index)
                queue_level[process_index] = 2
                arrival_time[process_index] = time
            else:
                time += local_burst_time
                if process_burst_index[process_index] <= len(processes[process_index]) - 3:
                    for i in range(len(processes)):
                        if ioreturn[i][1] == process_index:
                            ioreturn[i] = (processes[process_index][process_burst_index[process_index] + 1] + time, ioreturn[i][1])
                            break
                else:
                    complete[process_index] = 1
                process_burst_index[process_index] += 2
        elif ready_queue_rr2:
            process_index = ready_queue_rr2.popleft()

            # Update waiting time
            waiting_time[process_index] += time - arrival_time[process_index]
            local_burst_time = processes[process_index][process_burst_index[process_index]]

            # Print context switch data
            print_context_data(processes, process_index, ready_queue_rr2, process_burst_index, time)

            # Determine the action based on the remaining burst time
            if local_burst_time > tqrq2:
                time += tqrq2

                processes[process_index][process_burst_index[process_index]] = local_burst_time - tqrq2
                ready_queue_fcfs3.append(process_index)
                queue_level[process_index] = 3
                arrival_time[process_index] = time

            else:
                time += local_burst_time
                if process_burst_index[process_index] <= len(processes[process_index]) - 3:
                    for i in range(len(processes)):
                        if ioreturn[i][1] == process_index:
                            ioreturn[i] = (processes[process_index][process_burst_index[process_index] + 1] + time, ioreturn[i][1])
                            break
                else:
                    complete[process_index] = 1
                process_burst_index[process_index] += 2
        # Execute processes in the third queue
        elif ready_queue_fcfs3:
            process_index = ready_queue_fcfs3.popleft()

            # Update waiting time
            waiting_time[process_index] += time - arrival_time[process_index]

            # Print context switch data
            print_context_data(processes, process_index, ready_queue_fcfs3, process_burst_index, time)
            time += processes[process_index][process_burst_index[process_index]]

            if process_burst_index[process_index] <= len(processes[process_index]) - 3:
                for i in range(len(processes)):
                    if ioreturn[i][1] == process_index:
                        ioreturn[i] = (processes[process_index][process_burst_index[process_index] + 1] + time, ioreturn[i][1])
                        break
            else:
                complete[process_index] = 1
            process_burst_index[process_index] += 2
        # Sort ioreturn list
        ioreturn.sort()

        # Check for idle CPU time
        if not (ready_queue_rr1 or ready_queue_rr2 or ready_queue_fcfs3):
            while ioreturn[0][0] != maxsize and ioreturn[0][0] > time:
                time += 1
                idle_cpu_time += 1

        # Add processes to the appropriate queue based on the IO return time
        for i in range(len(processes)):
            if ioreturn[i][0] <= time:
                if queue_level[ioreturn[i][1]] == 1:
                    ready_queue_rr1.append(ioreturn[i][1])
                elif queue_level[ioreturn[i][1]] == 2:
                    ready_queue_rr2.append(ioreturn[i][1])
                else:
                    ready_queue_fcfs3.append(ioreturn[i][1])
                arrival_time[ioreturn[i][1]] = ioreturn[i][0]
                ioreturn[i] = (maxsize, ioreturn[i][1])

    burst_time = time - idle_cpu_time

    # Calculate Turnaround Time for each process
    for i in range(len(processes)):
        total_burst_time = sum(processes[i])
        tat[i] += total_burst_time + waiting_time[i]

    # Printing the results
    print(f"Total time: {len(processes)}")
    print(f"CPU Utilization: {burst_time / time * 100:.2f}%\n")

    print("Waiting Time")
    twt = sum(waiting_time)
    for i in range(len(processes)):
        print(f"Process: {i}, Waiting Time: {waiting_time[i]}")
    print(f"Average Waiting Time: {twt / len(processes)}\n")

    print("Turnaround Time")
    ttat = sum(tat)
    for i in range(len(processes)):
        print(f"Process: {i}, Turnaround Time: {tat[i]}")
    print(f"Average Turnaround Time: {ttat / len(processes)}\n")

    print("Response Time")
    trt = sum(response_time)
    for i in range(len(processes)):
        print(f"Process: {i}, Response Time: {response_time[i]}")
    print(f"Average Response Time: {trt / len(processes)}")

# Function to print the contents of a queue
def print_queue_contents(q, processes, process_burst_index):
    print(f"{'Process': <10} {'Burst': <10}")
    if q:
        for pid in q:
            print(f"P{pid: <10} {processes[pid][process_burst_index[pid]]: <10}")
    else:
        print(f"{'empty': <10} {'empty': <10}")
    print()

# Function to print completed processes
def print_processes(complete):
    completed_processes = [f"P{idx} " for idx, val in enumerate(complete) if val == 1]
    print("Complete Processes:", "".join(completed_processes))


# Function to print context switch data
def print_context_data(processes, process_index, ready_queue, process_burst_index, time):
    print(f"Current Execution Time: {time}\n")
    print(f"Next Process on the CPU: P{process_index}")
    print("Ready queue:")
    print_queue_contents(ready_queue, processes, process_burst_index)

if __name__ == '__main__':
    # Define the processes and initialize the queues and process burst index
    num_processes = 8
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

    ready_queue_rr1 = deque(range(num_processes))
    ready_queue_rr2 = deque()
    ready_queue_fcfs3 = deque()
    process_burst_index = [0] * num_processes

    print("MLFQ")
    # Execute the Multi-Level Feedback Queue Scheduling
    perform_mlfq(processes, ready_queue_rr1, process_burst_index)

























    










        

          
   





    
        

