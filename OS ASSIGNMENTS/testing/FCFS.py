import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import time
from tkinter import messagebox 

# Process class as in your original code
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

def FCFS(processes, result_label, canvas, root):
    current_time = 0
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        canvas.delete("all")  # Clear canvas before drawing animation
        draw_process_block(canvas, process.pid, "Running")
        root.update()  # Update GUI

        # Simulate execution time
        time.sleep(2)  # Short delay to simulate burst time execution
        
        current_time += process.remaining_time
        process.completion_time = current_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.remaining_time = 0
        process.utilization = (process.burst_time / process.turnaround_time) * 100

        # Update process info on label
        update_process_info(processes, result_label)
        time.sleep(1)

def update_process_info(processes, result_label):
    text = "PID\tArrival Time\tBurst Time\tCompletion Time\tTurnaround Time\tWaiting Time\tUtilization\n"
    for process in processes:
        text += (f"{process.pid}\t\t{process.arrival_time}\t\t{process.burst_time}\t\t"
                 f"{process.completion_time}\t\t{process.turnaround_time}\t\t"
                 f"{process.waiting_time}\t\t{process.utilization:.2f}%\n")
    result_label.config(text=text)

def draw_process_block(canvas, pid, status):
    # Drawing a process block on canvas with a colorful theme
    canvas.create_rectangle(50, 50, 250, 150, fill="skyblue", outline="black", width=3)
    canvas.create_text(150, 100, text=f"Process {pid}: {status}", font=('Arial', 16), fill="black")

def get_user_input(process_list, entry_widgets):
    # Reading input values from GUI with validation
    for i, entries in enumerate(entry_widgets):
        arrival_time_str = entries[0].get()
        burst_time_str = entries[1].get()

        # Check if the input fields are empty
        if not arrival_time_str or not burst_time_str:
            messagebox.showerror("Input Error", f"Please enter valid arrival and burst times for process {i}.")
            return

        try:
            # Convert the inputs to integers after validation
            arrival_time = int(arrival_time_str)
            burst_time = int(burst_time_str)
        except ValueError:
            # Show an error if the input cannot be converted to an integer
            messagebox.showerror("Input Error", f"Please enter valid integer values for process {i}.")
            return

        # Append validated process information to the process list
        process_list.append(Process(i, arrival_time, burst_time))

    return process_list

def start_fcfs(root, processes, result_label, canvas):
    # Sort processes by arrival time
    processes.sort(key=lambda p: p.arrival_time)
    FCFS(processes, result_label, canvas, root)

def create_gui():
    root = ThemedTk(theme="radiance")  # Use colorful theme
    root.title("FCFS Scheduler GUI")

    # Frame for Process Input
    frame = ttk.Frame(root)
    frame.pack(pady=20)

    ttk.Label(frame, text="Enter Process Details").grid(row=0, columnspan=4, pady=10)

    entry_widgets = []
    for i in range(3):  # For 3 processes as an example
        ttk.Label(frame, text=f"Process {i}").grid(row=i+1, column=0, padx=10)
        arrival_entry = ttk.Entry(frame)
        burst_entry = ttk.Entry(frame)
        arrival_entry.grid(row=i+1, column=1, padx=10)
        burst_entry.grid(row=i+1, column=2, padx=10)
        entry_widgets.append((arrival_entry, burst_entry))

    # Canvas for Animation
    canvas = tk.Canvas(root, width=300, height=200, bg="white")
    canvas.pack(pady=20)

    result_label = ttk.Label(root, text="", font=('Courier', 10), anchor="w")
    result_label.pack(pady=10)

    processes = []

    # Start FCFS button
    start_button = ttk.Button(frame, text="Start FCFS", command=lambda: start_fcfs(root, processes, result_label, canvas))
    start_button.grid(row=5, columnspan=3, pady=20)

    # Exit button
    exit_button = ttk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    # Function to get user input
    get_user_input(processes, entry_widgets)

    root.mainloop()

if __name__ == "__main__":
    create_gui()