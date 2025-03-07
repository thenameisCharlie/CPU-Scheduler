import sys
from queue import PriorityQueue

# Function to perform Shortest Job First scheduling
def perform_sjf_scheduling(processes, readyQueue, processBurstIndex):
    # List to store the time when each process returns from I/O
    ioreturn = [(sys.maxsize, i) for i in range(len(processes))]

    # Initializing lists for various metrics
    arrivalTime = [0] * len(processes) # List to store arrival time for each process
    waitingTime = [0] * len(processes) # List to store waiting time for each process
    tat = [0] * len(processes) # List to store turnaround time for each process
    responseTime = [-1] * len(processes) # List to store response time  for each process
    complete = [0] * len(processes) # List to keep track of completed processes

    time = 0 # Current time
    idle_Cpu_Time = 0 # Idle CPU time

    # Main loop for the scheduling
    while not readyQueue.empty():
        process_index = readyQueue.get()[1] # Get the process index from the ready queue

        # Calculating waiting time
        waitingTime[process_index] += time - arrivalTime[process_index]


        # Calculating response time
        if responseTime[process_index] == -1:
            responseTime[process_index] = time - arrivalTime[process_index]

        # Printing context switch data
        print_context_data(processes, process_index, readyQueue,processBurstIndex, time)

        # Incrementing time based on the burst time of the current process
        time += processes[process_index][processBurstIndex[process_index]]

        # Checking if the current process has more bursts
        if processBurstIndex[process_index] <= len(processes[process_index]) - 3:
            for i in range(len(ioreturn)):
                if ioreturn[i][1] == process_index:
                    ioreturn[i] = (processes[process_index][processBurstIndex[process_index] + 1] + time, process_index)
                    break
        
        else:
          complete[process_index] = 1 # Marking the process as complete

          
        # Printing the list of complete processes
        print_processes(complete)

        # Moving to the next burst index
        processBurstIndex[process_index] += 2
        ioreturn.sort()

        # Checking if the ready queue is empty
        if readyQueue.empty():
            while ioreturn[0][0] != sys.maxsize and ioreturn[0][0] > time:
                time += 1
                idle_Cpu_Time += 1 # Incrementing idle CPU time

        # Adding processes to the ready queue that have returned from I/O
        for i in range(len(ioreturn)):
            if ioreturn[i][0] <= time: 
                readyQueue.put((processes[ioreturn[i][1]][processBurstIndex[ioreturn[i][1]]], ioreturn[i][1]))
                arrivalTime[ioreturn[i][1]] = ioreturn[i][0]
                ioreturn[i] = (sys.maxsize, ioreturn[i][1])

    # Calculating burst time
    burst_time = time - idle_Cpu_Time

    # Calculating turnaround time for each process
    for i in range(len(processes)):
        tat[i] = sum(processes[i]) + waitingTime[i]

    # Printing various metrics
    print(f"Total time: {len(processes)}")
    print(f"CPU Utilization: {burst_time / time * 100:.2f}%\n")

    # Printing waiting time for each process
    print("\nWaiting Time")
    twt = sum(waitingTime)
    for i in range(len(processes)):
        print(f"Process: {i}, Waiting Time: {waitingTime[i]}")
    print(f"Average Waiting Time: {twt / len(processes)}")

    # Printing turnaround time for each process
    print("\nTurnaround Time")
    ttat = sum(tat)
    for i in range(len(processes)):
        print(f"Process: {i}, Turnaround Time: {tat[i]}")
    print(f"Average Turnaround Time: {ttat / len(processes)}")

    # Printing response time for each process
    print("\nResponse Time")
    trt = sum(responseTime)
    for i in range(len(processes)):
        print(f"Process: {i}, Response Time: {responseTime[i]}")
    print(f"Average Response Time: {trt / len(processes)}")

# Function to print the current state of the queue
def print_queue_state(q, processes, processBurstIndex):
    print(f"{'Process':<10}{'Burst':<10}")
    tempQ = PriorityQueue()
    if not q.empty():
        while not q.empty():
            item = q.get()
            tempQ.put(item)
            pid = item[1]

        print(f"P{pid:<9}{processes[pid][processBurstIndex[pid]]:<10}")
    else:
        print(f"{'empty': <10} {'empty': <10}")
    print()
    while not tempQ.empty():
        q.put(tempQ.get())


# Function to print the list of complete processes
def print_processes(complete):
    print("Complete Processes:", " ".join(f"P{i}" for i in range(len(complete)) if complete[i] == 1))  
        # Function to print context switch data

def print_context_data(processes, process_index, readyQueue,processBurstIndex, time):
    print(f"Current Execution Time: {time}\n")
    print(f"Next Process on the CPU: P{process_index}")
    print_queue_state(readyQueue, processes, processBurstIndex)


# Main block
if __name__ == "__main__":
    numProcesses = 8
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

    processBurstIndex = [0] * numProcesses # Initializing burst index for each process
    readyQueueSJF = PriorityQueue() # Creating a priority queue for the ready queue

    # Adding processes to the ready queue
    for i in range(len(processes)):
        readyQueueSJF.put((processes[i][processBurstIndex[i]], i))

    # Starting the SJF scheduling
    print("SJF")
    perform_sjf_scheduling(processes, readyQueueSJF, processBurstIndex)









