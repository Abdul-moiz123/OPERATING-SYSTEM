# first we have import queue from python module
from collections import deque

class Process:
    def __init__(self, pid, arrival_time, execution_time):
        self.pid = pid  # process ID
        self.arrival_time = arrival_time  # arrival time
        self.execution_time = execution_time  # execution time
        self.remaining_time = execution_time  # remaining execution time
        # calculation variables
        self.completion_time = 0  # completion time
        self.waiting_time = 0  # waiting time
        self.turnaround_time = 0  # turnaround time
        self.response_time = 0  # response time
        self.start_time = 0  # start time
        self.utilization = 0.0  # CPU utilization

def main():
    processes = []
    n = int(input("Enter total number of processes: "))
    time_quantum = int(input("\nEnter time quantum: "))
    current_time = 0
    completed = 0  # total processes completed
    sum_tat = 0  # total turnaround time
    sum_wt = 0  # total waiting time
    sum_rt = 0  # total response time
    sum_util = 0  # total utilization

    # Read arrival and execution times for each process
    for i in range(n):
        arrival_time = int(input(f"\nEnter Process {i} Arrival Time: "))
        execution_time = int(input(f"\nEnter Process {i} Execution Time: "))
        processes.append(Process(i, arrival_time, execution_time))

    # Sort processes by arrival time
    processes.sort(key=lambda p: p.arrival_time)

    # Initialize the ready queue and visited list
    ready_queue = deque()
    visited = [False] * n   # [false,false] --> [true.false] --> [true,true] --> complete

    # Start with the first process
    ready_queue.append(0) #process with id 0 --> first process --> process 0 add to queue
    visited[0] = True

# START FROM HERE --> Round Robin Algo

    while completed < n:
        index = ready_queue.popleft()  # hold the id of the process that is been dequeue --> index from where it is pop
        # single process 
        process = processes[index]

        # true if process just started
        if process.remaining_time == process.execution_time:
            process.start_time = max(current_time, process.arrival_time)
            current_time = process.start_time

        # true when process has already started and inthe middle
        if process.remaining_time > time_quantum:
            process.remaining_time -= time_quantum
            current_time += time_quantum
            
        # true when process has less remaining time than than quantum     
        else:
            current_time += process.remaining_time
            process.remaining_time = 0
            completed += 1

            # Update process statistics  --> now calculating all the factor
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.execution_time
            process.response_time = process.start_time - process.arrival_time
            process.utilization = (process.execution_time / process.turnaround_time) * 100

            # Accumulate statistics --> average of all the process
            sum_tat += process.turnaround_time
            sum_wt += process.waiting_time
            sum_rt += process.response_time
            sum_util += process.utilization

        # Check for new processes to add to the ready queue
        for i in range(n):
            if processes[i].remaining_time > 0 and processes[i].arrival_time <= current_time and not visited[i]:
                ready_queue.append(i)
                visited[i] = True

        # Push the current process back to the queue if it has remaining time
        if process.remaining_time > 0:
            ready_queue.append(index)

        # If the queue is empty, add a new process from the list
        if not ready_queue:
            for i in range(n):
                if processes[i].remaining_time > 0:
                    ready_queue.append(i)
                    visited[i] = True
                    break

    # Output results
    print("\nPID\tAT\tET\tST\tCT\tTAT\tWT\tRT\tUtil")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t{process.execution_time}\t{process.start_time}\t{process.completion_time}\t{process.turnaround_time}\t{process.waiting_time}\t{process.response_time}\t{process.utilization:.2f}%")

    print(f"\nAverage Turn Around Time = {sum_tat / n:.2f}")
    print(f"Average Waiting Time = {sum_wt / n:.2f}")
    print(f"Average Response Time = {sum_rt / n:.2f}")
    print(f"Average Utilization % = {sum_util / n:.2f}")

if __name__ == "__main__":
    main()