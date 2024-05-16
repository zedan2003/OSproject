import numpy as np
import matplotlib.pyplot as plt
import random

# Read inputs from file
with open('process.txt', 'r') as file:
    lines = file.readlines()

# Process input data
burst_times = np.array([int(x) for x in lines[0].strip().split(', ')], dtype='i')  # Burst times for each process
arrival_times = np.array([int(x) for x in lines[1].strip().split(', ')], dtype='i')  # Arrival times for each process
context_switch_duration = int(lines[2])  # Context switch duration
num_processes = int(lines[3])  # Number of processes


executed_times = np.zeros(num_processes, dtype='i')  # Array to keep track of executed times for each process


execution_log = [[]]  # List to store execution times for each process

# Function to record executed time
def record_execution(time, process_index):
    while process_index > len(execution_log) - 1:
        execution_log.append([])  # Ensure the list has enough sublists for all processes
    execution_log[process_index].append(time)  # Record the execution time
    return execution_log

# Initialize time and current process
current_time = 0  # Current time counter
current_process_index = -1  # Index of the current process being executed

# Sort processes by arrival time
sorted_indices = np.argsort(arrival_times)  # Get indices that would sort the arrival times
arrival_times = arrival_times[sorted_indices]  # Sort arrival times
burst_times = burst_times[sorted_indices]  # Sort burst times accordingly

# Simulate FCFS scheduling
for process_index in range(num_processes):
    if current_process_index != process_index:
        if current_process_index != -1:
            current_time += context_switch_duration  # Add context switch time if switching processes
        current_process_index = process_index  # Update current process index

    for _ in range(burst_times[process_index]):
        executed_times[process_index] += 1  # Increment executed time for the current process
        execution_log = record_execution(current_time, process_index)  # Record the execution time
        current_time += 1  # Increment current time

print(execution_log)

# Calculate exit times
exit_times = [max(execution_log[process_index]) + 1 for process_index in range(num_processes)]  # Calculate exit times
exit_times = np.array(exit_times)

# Calculate turnaround times
turnaround_times = exit_times - arrival_times  # Calculate turnaround times
print(turnaround_times)

# Calculate average turnaround time
average_turnaround_time = np.mean(turnaround_times)  # Calculate average turnaround time
print('\nAverage turnaround time: ', average_turnaround_time, '\n')

# Calculate waiting times
waiting_times = turnaround_times - burst_times  # Calculate waiting times
average_waiting_time = np.mean(waiting_times)  # Calculate average waiting time
print('\nAverage waiting time: ', average_waiting_time, '\n')

# Calculate CPU utilization
total_busy_time = np.sum(burst_times)  # Total time the CPU was busy
total_elapsed_time = max(exit_times) + context_switch_duration * (num_processes - 1)  # Total elapsed time including context switches
cpu_utilization = (total_busy_time / total_elapsed_time) * 100  # CPU utilization percentage

# Print CPU utilization details
print(f'Total busy time: {total_busy_time}')
print(f'Total elapsed time: {total_elapsed_time}')
print(f'\nCPU Utilization: {cpu_utilization:.2f}%\n')

# Generate Gantt chart
fig, gnt = plt.subplots()

def draw_gantt_chart(num_processes, execution_log):
    gnt.set_ylim(0, (10 * num_processes) + 20)  # Set y-axis limit based on number of processes
    max_time = max([max(p) for p in execution_log]) + 1  # Calculate the maximum time for x-axis limit
    gnt.set_xlim(0, max_time)

    gnt.set_xlabel('seconds')  # Label x-axis
    gnt.set_ylabel('Processor')  # Label y-axis

    y_ticks = [15 + 10 * i for i in range(num_processes)]  # Set y-ticks for each process
    gnt.set_yticks(y_ticks)
    y_tick_labels = [str(i + 1) for i in range(num_processes)]  # Label each process
    gnt.set_yticklabels(y_tick_labels)

    gnt.grid(True)  # Enable grid

    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
              'tab:olive', 'tab:cyan', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
              '#7f7f7f', '#bcbd22', '#17becf']  # List of colors for Gantt chart

    for process_index, log in enumerate(execution_log):
        color = random.choice(colors)  # Randomly choose a color for each process
        for time in log:
            gnt.broken_barh([(time, 1)], (10 * (process_index + 1), 9), facecolors=(color))  # Draw the Gantt chart

    plt.savefig("images/FCFS.png")  # Save the Gantt chart as an image

draw_gantt_chart(num_processes, execution_log)
