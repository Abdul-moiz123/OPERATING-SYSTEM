class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1  
        self.utilization = 0.0

def SRT(processes):
    current_time = 0
    completed = 0
    n = len(processes)
    processes.sort(key=lambda p: p.arrival_time)  # Sort processes by arrival time
    
    while completed != n:
        ongoing_process = None
        for process in processes:
            if process.arrival_time <= current_time and process.remaining_time > 0:
                if ongoing_process is None or process.remaining_time < ongoing_process.remaining_time:
                    ongoing_process = process
        
        if ongoing_process is None:
            current_time += 1  
            continue

        # Start executing the selected process
        if ongoing_process.response_time == -1:
            ongoing_process.response_time = current_time  
        # Process runs for one unit of time
        ongoing_process.remaining_time -= 1
        current_time += 1
        # If the process finishes, update its completion, turnaround, and waiting times
        if ongoing_process.remaining_time == 0:
            ongoing_process.completion_time = current_time
            ongoing_process.turnaround_time = ongoing_process.completion_time - ongoing_process.arrival_time
            ongoing_process.waiting_time = ongoing_process.turnaround_time - ongoing_process.burst_time
            ongoing_process.utilization = (ongoing_process.burst_time / ongoing_process.turnaround_time) * 100
            completed += 1

        # Print process info after each time unit for better visualization
        print(f"\nAt time {current_time}, after executing process {ongoing_process.pid}:")
        print_process_info(processes)

def print_process_info(processes):
    print("PID\tArrival_time\tBurst_time\tCompletion_time\tTurnaround_time\tWaiting_time\tRemaining_time\tUtilization")
    for process in processes:
        print(f"{process.pid}\t\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.completion_time}\t\t{process.turnaround_time}\t\t{process.waiting_time}\t\t{process.remaining_time}\t\t{process.utilization:.2f}%")

def get_user_input():
    processes = []
    n = int(input("Enter the number of processes: "))
    for i in range(n):
        pid = i
        arrival_time = int(input(f"Enter Arrival Time for process {pid}: "))
        burst_time = int(input(f"Enter Burst Time for process {pid}: "))
        processes.append(Process(pid, arrival_time, burst_time))
    return processes

if __name__ == "__main__":
    processes = get_user_input()
    SRT(processes)