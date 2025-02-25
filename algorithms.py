from collections import deque
import heapq
from tabulate import tabulate

# Data provided by the assignment for the algorithms
process_data = {"p1":[5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4],
                "p2":[4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8],
                "p3":[8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6],
                "p4":[3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3],
                "p5":[16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4],
                "p6":[11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8],
                "p7":[14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10],
                "p8":[4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]}


#User input to determine which algorithm to run
algorithmSelection = input("Please choose an algorithm to run: \n1. First Come First Serve (FCFS)\n2. Shortest Job First (SJF)\n3. Multilevel Feedback Queue Scheduling (MLFQ)\n")


#Function that runs the First Come First Serve (FCFS) algorithm
def FCFS(process_data):

    ready_queue = deque(process_data.keys())
    io_queue = [] #min-heap queue will track I/O to ensure first in first out
    systemCurrentTime = 0 
    executionOrder = [] #This list will store the order in which the processes are executed 

    completionTimeList = {} #This dictionary will store the completion time for each process (will be used for calculating turnaround time)
    firstCPUTime = {} #This dictionary will store the first CPU time for each process (will be used for calculating response time)
    totalCPUTime = {p: sum(process_data[p][::2]) for p in process_data} #This dictionary will store the total CPU time for each process (will be used for calculating CPU utilization/waiting times)
    systemIdleTime = 0

        while ready_queue or io_queue:
            if ready_queue:
                current_process = ready_queue.popleft() #get the first process in the queue
                bursts = process_data[current_process] #get the burst times for the current process
                print("Current Process: ", current_process)

            if bursts:
                cpu_burst = bursts.pop(0) #Runs the process for the CPU burst time
                print(f"🔹 Running Process: {current_process} (CPU Burst: {cpu_burst})")
                systemCurrentTime += cpu_burst #increment the current time by the CPU burst time     
                print(f"🔹 Time {systemCurrentTime}: {current_process} finished CPU burst")  

                if not bursts: 
                    completionTimeList[current_process] = systemCurrentTime        

                if bursts:
                    io_burst = bursts.pop(0)
                    completionTime = systemCurrentTime + io_burst #total time a process waits and executes
                    heapq.heappush(io_queue, (completionTime, current_process)) #using a min-heap to track I/O burst using tuple (completionTime, process)
                    print(f"🔹 Time {systemCurrentTime}: {current_process} performing I/O for {io_burst} units")
            
        if not ready_queue and io_queue:
            systemIdleTime += max(0, io_queue[0][0] - systemCurrentTime) #calculate the system idle time (max() ensures that the idle time is not negative)
            systemCurrentTime = io_queue[0][0] #if the ready queue is empty, set the current time to the completion time of the first process in the I/O queue
            print(f"🔹 Time {systemCurrentTime}: System is idle") #debugging purposes
            print(f"{systemIdleTime} units of idle time") #debugging purposes
            
        

        #Check if the I/O queue is not empty and the first process in the queue has a completion time less than or equal to the current time to return to the ready queue
        while io_queue and io_queue[0][0] <= systemCurrentTime:
            completionTime, current_process = heapq.heappop(io_queue) #pop the first process in the I/O queue and assign it to the current process
            systemCurrentTime = completionTime
            ready_queue.append(current_process) 
            print(f"🔹 Time {systemCurrentTime}: {current_process} finished I/O and moved back to Ready Queue")


    return executionOrder, completionTimeList, firstCPUTime, totalCPUTime, systemCurrentTime, systemIdleTime

#function that computes Ttr, Tw, Tr for each process
def calculate_metrics(completionTimeList, firstCPUTime, totalCPUTime):
    turnaroundTimes = {}
    waitingTimes = {}
    responseTimes = {}

    totalProcesses = len(completionTimeList)

    totalTurnaroundTime = 0
    totalWaitingTime = 0
    totalResponseTime = 0

    # Calculate Ttr, Tw, Tr for each process
    for process in completionTimeList:
        Ttr = completionTimeList[process]
        Tw = Ttr - totalCPUTime[process]
        Tr = firstCPUTime[process]

        turnaroundTimes[process] = Ttr
        waitingTimes[process] = Tw
        responseTimes[process] = Tr

        totalTurnaroundTime += Ttr
        totalWaitingTime += Tw
        totalResponseTime += Tr

    avgTurnaroundTime = totalTurnaroundTime / totalProcesses
    avgWaitingTime = totalWaitingTime / totalProcesses
    avgResponseTime = totalResponseTime / totalProcesses

    return turnaroundTimes, waitingTimes, responseTimes, avgTurnaroundTime, avgWaitingTime, avgResponseTime


#Function that calculates the CPU utilization 
def calculate_cpu_utilization(systemCurrentTime, systemIdleTime):
    
    totalCPUExecutionTime = systemCurrentTime - systemIdleTime # Total time spent executing processes (excluding idle time)
    cpuUtilization = (totalCPUExecutionTime / systemCurrentTime) * 100
    print(f"Total CPU Execution Time: {totalCPUExecutionTime} units")
    print(f"Total System Time: {systemCurrentTime} units")
    
    return cpuUtilization


#Print the results of the simulation
def print_results(systemCurrentTime, cpuUtilization, avgTurnaroundTime, avgWaitingTime, avgResponseTime, completionTimeList, waitingTimes, firstCPUTime):
    print("\n🔹 **Final Simulation Results**")
    print(f"Total Time to Complete All Processes: {systemCurrentTime} units")
    print(f"CPU Utilization: {cpuUtilization:.2f}%")
    print(f"Avg Waiting Time (Tw): {avgWaitingTime:.2f}")
    print(f"Avg Turnaround Time (Ttr): {avgTurnaroundTime:.2f}")
    print(f"Avg Response Time (Tr): {avgResponseTime:.2f}")

        # Create table of per-process breakdown
    tableData = [[p, completionTimeList[p], waitingTimes[p], firstCPUTime[p]]
        for p in sorted(completionTimeList.keys())]
    
    # Print table of per-process breakdown
    print("\n🔹 **Per-Process Breakdown**")
    print(tabulate(tableData, headers=["Process", "Completion Time (Ttr)", "Waiting Time (Tw)", "Response Time (Tr)"], tablefmt="fancy_grid"))



#conditions that will determine which algorithm to run
if algorithmSelection == "1":
    executionOrder, completionTimeList, firstCPUTime, totalCPUTime, systemCurrentTime, systemIdleTime  = FCFS(process_data)
    turnaroundTimes, waitingTimes, responseTimes, avgTurnaroundTime, avgWaitingTime, avgResponseTime = calculate_metrics(completionTimeList, firstCPUTime, totalCPUTime)
    cpuUtilization = calculate_cpu_utilization(systemCurrentTime, systemIdleTime)
    print_results(systemCurrentTime, cpuUtilization, avgTurnaroundTime, avgWaitingTime, avgResponseTime, completionTimeList, waitingTimes, firstCPUTime)


elif algorithmSelection == "2":
    print(SJF(process_data))
    
elif algorithmSelection == "3":
    print(MLFQ(process_data))

else:
    print("Invalid input. Please try again.")



    





