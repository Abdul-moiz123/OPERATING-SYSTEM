class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_ratio = 0
        self.utilization = 0.0

def HRRN(processes):
    current_time = 0
    completed = 0
    n = len(processes)
    processes.sort(key=lambda p: p.arrival_time)  # Sort by arrival time initially

    while completed != n:
        # Calculate response ratio for all processes that have arrived and are not yet completed
        highest_response_process = None
        for process in processes:
            if process.arrival_time <= current_time and process.remaining_time > 0:
                # Calculate waiting time and response ratio
                waiting_time = current_time - process.arrival_time
                response_ratio = (waiting_time + process.burst_time) / process.burst_time
                process.response_ratio = response_ratio

                # Select the process with the highest response ratio
                if highest_response_process is None or process.response_ratio > highest_response_process.response_ratio:
                    highest_response_process = process

        if highest_response_process is None:
            # If no process has arrived yet, move the time forward
            current_time += 1
            continue

        # Execute the selected process (non-preemptive, so it runs to completion)
        current_time += highest_response_process.remaining_time
        highest_response_process.completion_time = current_time
        highest_response_process.turnaround_time = highest_response_process.completion_time - highest_response_process.arrival_time
        highest_response_process.waiting_time = highest_response_process.turnaround_time - highest_response_process.burst_time
        highest_response_process.remaining_time = 0  # Process completed
        highest_response_process.utilization = (highest_response_process.burst_time / highest_response_process.turnaround_time) * 100
        completed += 1

        print(f"\nAfter executing process {highest_response_process.pid}:")
        print_process_info(processes)

def print_process_info(processes):
    print("PID\tArrival_time\tBurst_time\tCompletion_time\tTurnaround_time\tWaiting_time\tRemaining_time\tUtilization\tResponse_ratio")
    for process in processes:
        print(f"{process.pid}\t\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.completion_time}\t\t{process.turnaround_time}\t\t{process.waiting_time}\t\t{process.remaining_time}\t\t{process.utilization:.2f}%\t\t{process.response_ratio:.2f}")

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
    HRRN(processes)
