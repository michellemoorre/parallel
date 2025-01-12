import numpy as np
import time
import multiprocessing as mp

def process_chunk(args):
    """Process a chunk of indices to compute concordant and discordant pairs."""
    start_i, end_i, x, y = args
    concordant = 0
    discordant = 0
    
    for i in range(start_i, end_i):
        for j in range(i + 1, len(x)):
            x_diff = x[i] - x[j]
            y_diff = y[i] - y[j]
            
            if x_diff * y_diff > 0:
                concordant += 1
            elif x_diff * y_diff < 0:
                discordant += 1
    
    return concordant, discordant

def parallel_kendall_correlation(x, y, n_processes=None):
    """
    Calculate Kendall rank correlation coefficient in parallel.
    
    Args:
        x (numpy.ndarray): First array of values
        y (numpy.ndarray): Second array of values
        n_processes (int): Number of processes to use (default: None, uses CPU count)
    
    Returns:
        float: Kendall correlation coefficient
    """
    if n_processes is None:
        n_processes = mp.cpu_count()
    
    n = len(x)
    # Calculate total number of pairs
    total_pairs = n * (n - 1) // 2
    
    # Split work into chunks based on the first index
    chunk_size = max(1, (n - 1) // n_processes)
    
    # Prepare arguments for each process
    args = []
    for start_i in range(0, n - 1, chunk_size):
        end_i = min(start_i + chunk_size, n - 1)
        args.append((start_i, end_i, x, y))
    
    # Process chunks in parallel
    with mp.Pool(processes=n_processes) as pool:
        results = pool.map(process_chunk, args)
    
    # Combine results
    total_concordant = sum(r[0] for r in results)
    total_discordant = sum(r[1] for r in results)
    
    # Calculate tau
    tau = (total_concordant - total_discordant) / total_pairs
    
    return tau

def main():
    # Load data
    try:
        x = np.load('data/x.npy')
        y = np.load('data/y.npy')
    except FileNotFoundError:
        print("Data files not found. Please run generate_data.py first.")
        return
    
    # Get total CPU count
    total_cpus = mp.cpu_count()
    # Limit max workers to 8 (reasonable for M3 Pro) and start from 2
    max_workers = min(8, total_cpus)
    n_processes_list = list(range(2, max_workers + 1))
    
    results = []
    
    print(f"Computing parallel Kendall correlation for {len(x)} samples...")
    print(f"Testing with 2 to {max_workers} workers...")
    
    for n_processes in n_processes_list:
        print(f"\nUsing {n_processes} processes...")
        
        start_time = time.time()
        tau = parallel_kendall_correlation(x, y, n_processes)
        end_time = time.time()
        
        execution_time = end_time - start_time
        results.append((n_processes, tau, execution_time))
        
        print(f"Kendall correlation coefficient: {tau:.4f}")
        print(f"Execution time: {execution_time:.2f} seconds")
    
    # Save results for comparison
    with open('results_parallel.txt', 'w') as f:
        f.write("Parallel Implementation Results\n")
        f.write(f"Number of samples: {len(x)}\n")
        for n_proc, tau, exec_time in results:
            f.write(f"\nProcesses: {n_proc}\n")
            f.write(f"Kendall correlation coefficient: {tau:.4f}\n")
            f.write(f"Execution time: {exec_time:.2f} seconds\n")

if __name__ == '__main__':
    main() 