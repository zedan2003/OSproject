import numpy as np
import matplotlib.pyplot as plt
import random

# Read process data from file
with open('process.txt', 'r') as file:
    file_lines = file.readlines()

# Process file data
burst_times = np.array([int(x) for x in file_lines[0].strip().split(', ')], dtype='i')  # Burst times of each process
arrival_times = np.array([int(x) for x in file_lines[1].strip().split(', ')], dtype='i')  # Arrival times of each process
context_switch_duration = int(file_lines[2])  # Duration of context switch
num_processes = int(file_lines[3])  # Number of processes

# Initialize variables
current_time = 0  # Current time in the simulation
executed_times = np.zeros(num_processes, dtype='i')  # Array to keep track of executed times for each process
remaining_times = burst_times.copy()  # Array to keep track of remaining burst times for each process
process_execution_log = [[] for _ in range(num_processes)]  # Log of execution times for each process
current_process_index = -1  # Index of the current process being executed

# Function to get ready queue at a given time
def get_ready_queue(time, arrival_times):
    return np.where(arrival_times <= time)[0]

# Function to update executed time of a process
def update_executed_time(exec_times, process_index):
    exec_times[process_index] += 1
    return exec_times

# Function to update remaining time of a process
def update_remaining_time(remain_times, process_index):
    remain_times[process_index] -= 1
    return remain_times

# Function to record process execution
def log_process_execution(time, process_index):
    process_execution_log[process_index].append(time)
    return process_execution_log

# Function to find the process with the shortest remaining time
def find_shortest_remaining_time(remaining_times, ready_queue):
    adjusted_times = np.where(remaining_times > 0, remaining_times, np.inf)
    while True:
        min_time = np.min(adjusted_times)
        candidates = np.where(remaining_times == min_time)[0]
        for candidate in candidates:
            if candidate in ready_queue:
                return candidate
        adjusted_times[candidates] = np.inf

# Main simulation loop
while np.any(remaining_times > 0):
    ready_queue = get_ready_queue(current_time, arrival_times)  # Get processes that have arrived by current time
    next_process_index = find_shortest_remaining_time(remaining_times, ready_queue)  # Find the process with the shortest remaining time
    
    if current_process_index != next_process_index:  # Check if there is a context switch
        if current_process_index != -1:
            current_time += context_switch_duration  # Add context switch duration to current time
        current_process_index = next_process_index
    
    executed_times = update_executed_time(executed_times, current_process_index)  # Update executed time for the current process
    remaining_times = update_remaining_time(remaining_times, current_process_index)  # Update remaining time for the current process
    process_execution_log = log_process_execution(current_time, current_process_index)  # Log execution time for the current process
    current_time += 1  # Move to the next time unit

# Calculate exit times
exit_times = np.array([max(log) + 1 for log in process_execution_log])

# Calculate turnaround times
turnaround_times = exit_times - arrival_times

# Calculate average turnaround time
avg_turnaround_time = np.mean(turnaround_times)

# Calculate waiting times
waiting_times = turnaround_times - burst_times

# Calculate average waiting time
avg_waiting_time = np.mean(waiting_times)

# Calculate CPU utilization
total_busy_time = np.sum(burst_times)
total_elapsed_time = max(exit_times) + context_switch_duration * (num_processes - 1)
cpu_utilization = (total_busy_time / total_elapsed_time) * 100

# Print results

print(f'\nAverage turnaround time: {avg_turnaround_time}\n')
print(f'\nAverage waiting time: {avg_waiting_time}\n')
print(f'\nTotal busy time: {total_busy_time}')
print(f'Total elapsed time: {total_elapsed_time}')
print(f'CPU Utilization: {cpu_utilization:.2f}%\n')

# Generate Gantt chart
def generate_gantt_chart(num_processes, execution_log):
    fig, gantt_chart = plt.subplots()
    gantt_chart.set_ylim(0, (10 * num_processes) + 20)
    max_time = max([max(p) for p in execution_log]) + 1
    gantt_chart.set_xlim(0, max_time)
    gantt_chart.set_xlabel('seconds')
    gantt_chart.set_ylabel('Processor')
    y_ticks = [15 + 10 * i for i in range(num_processes)]
    gantt_chart.set_yticks(y_ticks)
    gantt_chart.set_yticklabels([str(i + 1) for i in range(num_processes)])
    gantt_chart.grid(True)
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
              'tab:olive', 'tab:cyan', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
              '#7f7f7f', '#bcbd22', '#17becf']
    
    for i, log in enumerate(execution_log):
        color = random.choice(colors)  # Choose a random color for each process
        for time in log:
            gantt_chart.broken_barh([(time, 1)], (10 * (i + 1), 9), facecolors=(color))  # Draw the execution block
    
    plt.savefig("images/SRT.png")

generate_gantt_chart(num_processes, process_execution_log)
