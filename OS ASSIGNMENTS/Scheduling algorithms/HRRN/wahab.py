import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_ratio = 0.0
        self.utilization = 0.0

def HRRN(processes):
    current_time = 0
    completed = 0
    gantt_chart = []  # To store Gantt chart information

    while completed < len(processes):
        # Calculate response ratio for all processes that have arrived and are not yet completed
        highest_response_process = None
        for process in processes:
            if process.arrival_time <= current_time and process.remaining_time > 0:
                # Calculate waiting time and response ratio
                waiting_time = current_time - process.arrival_time
                response_ratio = (waiting_time + process.burst_time) / process.burst_time
                process.response_ratio = response_ratio

                # Select the process with the highest response ratio
                if highest_response_process is None or response_ratio > highest_response_process.response_ratio:
                    highest_response_process = process

        if highest_response_process is None:
            # If no process has arrived yet, move the time forward
            current_time += 1
            continue

        # Execute the selected process (non-preemptive, so it runs to completion)
        start_time = current_time
        current_time += highest_response_process.remaining_time
        end_time = current_time
        gantt_chart.append((highest_response_process.pid, start_time, end_time))  # (PID, Start, End)

        # Update process info
        highest_response_process.completion_time = end_time
        highest_response_process.turnaround_time = highest_response_process.completion_time - highest_response_process.arrival_time
        highest_response_process.waiting_time = highest_response_process.turnaround_time - highest_response_process.burst_time
        highest_response_process.remaining_time = 0  # Process completed
        highest_response_process.utilization = (highest_response_process.burst_time / highest_response_process.turnaround_time) * 100
        completed += 1

        print(f"\nAfter executing process {highest_response_process.pid}:")
        print_process_info(processes)

    plot_gantt_chart(gantt_chart)

def print_process_info(processes):
    print("\nPID\tArrival_time\tBurst_time\tCompletion_time\tTurnaround_time\tWaiting_time\tRemaining_time\tUtilization")
    for process in processes:
        print(f"{process.pid}\t\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.completion_time}\t\t{process.turnaround_time}\t\t{process.waiting_time}\t\t{process.remaining_time}\t\t{process.utilization:.2f}%")

def plot_gantt_chart(gantt_chart):
    fig, ax = plt.subplots(figsize=(10, 3))
    colors = plt.get_cmap("tab10")  # Color palette

    for i, (pid, start, end) in enumerate(gantt_chart):
        ax.barh(1, end - start, left=start, color=colors(i % 10), edgecolor="black", height=0.5)
        ax.text((start + end) / 2, 1, f"P{pid}", ha='center', va='center', color="white", fontweight="bold")

    ax.set_yticks([])
    ax.set_xticks(range(0, gantt_chart[-1][2] + 1))
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart of HRRN Scheduling")

    plt.show()

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
    processes.sort(key=lambda p: p.arrival_time)  # Sort processes by arrival time
    HRRN(processes)
