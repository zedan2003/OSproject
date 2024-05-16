import numpy as np
import matplotlib.pyplot as plt
import random

# Import necessary libraries: numpy for numerical operations, matplotlib for plotting, and random for random color selection

# Get inputs from a text file
with open('process.txt', 'r') as file:
    lines = file.readlines()  # Read the entire content of the file line by line

lines[0] = lines[0].replace('\n', '')  # Remove newline character from the first line
lines[1] = lines[1].replace('\n', '')  # Remove newline character from the second line

burst_times = np.array([int(x) for x in lines[0].split(', ')], dtype='i')  # Convert burst times from the first line to numpy array
arrival_times = np.array([int(x) for x in lines[1].split(', ')], dtype='i')  # Convert arrival times from the second line to numpy array
context_switch_duration = int(lines[2])  # Read the context switch duration from the third line
num_processes = int(lines[3])  # Read the number of processes from the fourth line
time_quantum = int(lines[4])  # Read the time quantum from the fifth line

# Initialize executed times array for each process
executed_times = np.zeros(num_processes, dtype='i')  

def update_executed_time(arr, idx):
    arr[idx] += 1  # Increment the executed time for a specific process
    return arr

# Initialize remaining times array, copying from burst_times
remaining_times = burst_times.copy()

def update_remaining_time(rt, idx):
    rt[idx] -= 1  # Decrement the remaining time for a specific process
    return rt

# Determine which processes are ready to be executed
current_time = 0  # Start the simulation at time zero

def ready_queue(current_time, arrival_times, burst_times, executed_times):
    queue = np.where(arrival_times <= current_time, True, False)  # Check if processes have arrived by the current time
    for idx in range(num_processes):
        if burst_times[idx] <= executed_times[idx]:
            queue[idx] = False  # Exclude processes that have completed their burst times
    return queue

# Update inQT (index of QT process)
def update_inQT(ready_indices, inQT, qt, time_quantum, remaining_times, executed_times, burst_times):
    for idx in ready_indices:
        if idx not in inQT:
            inQT = np.append(inQT, idx)  # Add new ready process to inQT
            qt = np.append(qt, time_quantum)  # Assign time quantum for new processes

    for idx in inQT:
        if idx not in ready_indices:
            del_idx = int(np.where(inQT == idx)[0])
            inQT = np.delete(inQT, del_idx)  # Remove processes no longer ready
            qt = np.delete(qt, del_idx)  # Adjust time quantum array

    if qt[0] <= 0:
        if executed_times[inQT[0]] == burst_times[inQT[0]] and remaining_times[inQT[0]] <= 0:
            inQT = np.delete(inQT, 0)  # Remove process that has completed its burst time
            qt = np.delete(qt, 0)
        else:
            temp = inQT[0]
            inQT[:-1] = inQT[1:]  # Rotate the queue
            inQT[-1] = temp
            qt[0] = time_quantum  # Reassign time quantum to the rotated process
    else:
        qt[0] -= 1  # Decrement time quantum for the current process

    return qt, inQT

# Create a list of lists to record process execution at each time unit
process_execution = [[] for _ in range(num_processes)]

# Record execution times
def record_execution(time, process_idx):
    process_execution[process_idx].append(time)  # Append current time to the execution list of the process
    return process_execution

# Initialize variables
time = 0  # Start time
inQT = np.array([], dtype='i')  # Initialize empty array for inQT
qt = np.array([], dtype='i')  # Initialize empty array for quantum times
current_process_idx = -1  # Start with no current process

# Main simulation loop
while not (executed_times == burst_times).all():  # Continue until all processes have finished execution
    ready = ready_queue(time, arrival_times, burst_times, executed_times)  # Determine which processes are ready
    ready_indices = np.where(ready == True)[0]  # Get indices of ready processes
    qt, inQT = update_inQT(ready_indices, inQT, qt, time_quantum, remaining_times, executed_times, burst_times)  # Update quantum times and inQT
    next_process_idx = inQT[0]  # Select the next process to execute

    if current_process_idx != next_process_idx:
        if current_process_idx != -1:
            time += context_switch_duration  # Add context switch duration if switching processes
        current_process_idx = next_process_idx  # Update current process index

    executed_times = update_executed_time(executed_times, next_process_idx)  # Update executed time for current process
    remaining_times = update_remaining_time(remaining_times, next_process_idx)  # Update remaining time for current process
    process_execution = record_execution(time, next_process_idx)  # Record execution for the current process

    time += 1  # Increment time

print(process_execution)  # Print the process execution record

# Calculate exit times
exit_times = np.array([max(proc) + 1 for proc in process_execution])  # Calculate exit times for each process
print(exit_times)  # Print exit times

# Calculate turnaround times
turnaround_times = exit_times - arrival_times  # Calculate turnaround times for each process
print(turnaround_times)  # Print turnaround times

# Calculate average turnaround time
average_turnaround_time = np.mean(turnaround_times)
print('\nAverage turnaround time:', average_turnaround_time)  # Print average turnaround time

# Calculate average waiting time
waiting_times = turnaround_times - burst_times  # Calculate waiting times for each process
average_waiting_time = np.mean(waiting_times)
print('\nAverage waiting time:', average_waiting_time)  # Print average waiting time

# Calculate CPU utilization
total_busy_time = sum(burst_times)  # Total time that the CPU was busy
total_elapsed_time = max(exit_times) + context_switch_duration * (num_processes - 1)  # Total time elapsed including context switches
cpu_utilization = (total_busy_time / total_elapsed_time) * 100  # Calculate CPU utilization percentage
print(f'\nTotal busy time: {total_busy_time}')  # Print total busy time
print(f'Total elapsed time: {total_elapsed_time}')  # Print total elapsed time
print(f'CPU Utilization: {cpu_utilization:.2f}%\n')  # Print CPU utilization

# Gantt chart
fig, gantt_chart = plt.subplots()  # Create a subplot for Gantt chart

def plot_gantt_chart(num_processes, process_execution):
    gantt_chart.set_ylim(0, (10 * num_processes) + 20)  # Set the limits for y-axis
    max_time = max([max(proc) for proc in process_execution]) + 1  # Calculate the maximum time for x-axis
    gantt_chart.set_xlim(0, max_time)  # Set the limits for x-axis

    gantt_chart.set_xlabel('Time (seconds)')  # Set x-axis label
    gantt_chart.set_ylabel('Process')  # Set y-axis label

    y_ticks = [15 + 10 * i for i in range(num_processes)]  # Set y-ticks positions
    gantt_chart.set_yticks(y_ticks)  # Apply y-ticks
    gantt_chart.set_yticklabels([str(i + 1) for i in range(num_processes)])  # Label y-ticks with process numbers
    gantt_chart.grid(True)  # Enable grid for easier visualization

    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
              'tab:olive', 'tab:cyan', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
              '#7f7f7f', '#bcbd22', '#17becf']  # Define a list of colors for processes

    for proc_idx, proc_times in enumerate(process_execution):
        color = random.choice(colors)  # Randomly select a color for each process
        for time in proc_times:
            gantt_chart.broken_barh([(time, 1)], (10 * (proc_idx + 1), 9), facecolors=(color))  # Draw bars for each time unit of process execution

    plt.savefig("images/RR.png")  # Save the Gantt chart as an image file

plot_gantt_chart(num_processes, process_execution)  # Call the function to plot Gantt chart
