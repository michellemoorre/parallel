import matplotlib.pyplot as plt
import numpy as np
import re

def parse_results_file(filename):
    """Parse the results file to extract execution times."""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Extract execution times
    times = re.findall(r"Execution time: ([\d.]+) seconds", content)
    return [float(t) for t in times]

def create_speedup_plot():
    """Create and save the speedup plot."""
    # Get sequential time (baseline)
    sequential_times = parse_results_file('results_sequential.txt')
    sequential_time = sequential_times[0]
    
    # Get parallel times
    parallel_times = parse_results_file('results_parallel.txt')
    
    # Calculate speedup
    n_processes = list(range(1, len(parallel_times) + 1))
    speedups = [sequential_time / t for t in parallel_times]
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(n_processes, speedups, 'bo-', label='Actual speedup')
    plt.plot(n_processes, n_processes, 'r--', label='Linear speedup (ideal)')
    
    plt.xlabel('Number of Processes')
    plt.ylabel('Speedup (Sequential time / Parallel time)')
    plt.title('Kendall Correlation Speedup vs Number of Processes')
    plt.grid(True)
    plt.legend()
    
    # Save plot
    plt.savefig('speedup_plot.png')
    plt.close()

def main():
    try:
        create_speedup_plot()
        print("Speedup plot has been generated as 'speedup_plot.png'")
    except FileNotFoundError:
        print("Results files not found. Please run sequential_kendall.py and parallel_kendall.py first.")

if __name__ == '__main__':
    main() 