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
        self.response_time = 0
        self.utilization = 0.0

def FCFS(processes):
    current_time = 0
    gantt_chart = []  # To store Gantt chart info

    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time  # Process starts as it arrives
        
        start_time = current_time
        current_time += process.remaining_time  # Update current time by execution time
        end_time = current_time
        gantt_chart.append((process.pid, start_time, end_time))  

        process.completion_time = end_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.remaining_time = 0
        process.utilization = (process.burst_time / process.turnaround_time) * 100

        print(f"\nAfter executing process {process.pid}:")
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
    ax.set_title("Gantt Chart of FCFS Scheduling")

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
    processes.sort(key=lambda p: p.arrival_time)
    FCFS(processes)
