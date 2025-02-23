from collections import deque
import heapq

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

#Function with the FCFS algorithm implementation 
if algorithmSelection == "1":
    def FCFS(process_data):

        ready_queue = deque(process_data.keys())
        io_queue = [] #min-heap queue will track I/O to ensure first in first out
        systemCurrentTime = 0

        while ready_queue or io_queue:
            if ready_queue:
                current_process = ready_queue.popleft() #get the first process in the queue
                bursts = process_data[current_process] #get the burst times for the current process
                print("Current Process: ", current_process)

                if bursts:
                    cpu_burst = bursts.pop(0) #Runs the process for the CPU burst time
                    print(f"Time {systemCurrentTime}: {current_process} running for {cpu_burst} units")
                    systemCurrentTime += cpu_burst #increment the current time by the CPU burst time
                    print(f"Time {systemCurrentTime}: {current_process} finished CPU burst")

                    if bursts:
                        io_burst = bursts.pop(0)
                        completionTime = systemCurrentTime + io_burst #total time a process waits and executes
                        heapq.heappush(io_queue, (completionTime, current_process)) #using a min-heap to track I/O burst
                        print(f"Time {systemCurrentTime}: {current_process} performing I/O for {io_burst} units")
            
            #If ready queue is empty, jump to the next I/O completion time
            if not ready_queue and io_queue:
                systemCurrentTime = io_queue[0][0]

            #Check if the I/O queue is not empty and the first process in the queue has a completion time less than or equal to the current time
            while io_queue and io_queue[0][0] <= systemCurrentTime:
                completionTime, current_process = heapq.heappop(io_queue) #pop the first process in the I/O queue and assign it to the current process
                systemCurrentTime = completionTime #update the current time to the completion time 
                ready_queue.append(current_process)
                print(f"Time {systemCurrentTime}: {current_process} finished I/O")
            
            
    
    print(FCFS(process_data))