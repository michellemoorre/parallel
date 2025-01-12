import numpy as np
import time

def kendall_correlation(x, y):
    """
    Calculate Kendall rank correlation coefficient sequentially.
    
    Args:
        x (numpy.ndarray): First array of values
        y (numpy.ndarray): Second array of values
    
    Returns:
        float: Kendall correlation coefficient
    """
    n = len(x)
    concordant = 0
    discordant = 0
    
    for i in range(n-1):
        for j in range(i+1, n):
            # Check if pairs are concordant or discordant
            x_diff = x[i] - x[j]
            y_diff = y[i] - y[j]
            
            if x_diff * y_diff > 0:
                concordant += 1
            elif x_diff * y_diff < 0:
                discordant += 1
    
    # Calculate tau
    total_pairs = n * (n - 1) // 2
    tau = (concordant - discordant) / total_pairs
    
    return tau

def main():
    # Load data
    try:
        x = np.load('data/x.npy')
        y = np.load('data/y.npy')
    except FileNotFoundError:
        print("Data files not found. Please run generate_data.py first.")
        return
    
    print(f"Computing Kendall correlation for {len(x)} samples...")
    
    # Measure execution time
    start_time = time.time()
    tau = kendall_correlation(x, y)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    print(f"Kendall correlation coefficient: {tau:.4f}")
    print(f"Execution time: {execution_time:.2f} seconds")
    
    # Save results for comparison
    with open('results_sequential.txt', 'w') as f:
        f.write(f"Sequential Implementation Results\n")
        f.write(f"Number of samples: {len(x)}\n")
        f.write(f"Kendall correlation coefficient: {tau:.4f}\n")
        f.write(f"Execution time: {execution_time:.2f} seconds\n")

if __name__ == '__main__':
    main() 