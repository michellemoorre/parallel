import numpy as np
import os

def generate_data(n_samples=100000, seed=42):
    """Generate random data for Kendall correlation testing."""
    np.random.seed(seed)
    
    # Generate two correlated arrays with some noise
    x = np.random.normal(0, 1, n_samples)
    noise = np.random.normal(0, 0.5, n_samples)
    y = x + noise
    
    # Save the data
    if not os.path.exists('data'):
        os.makedirs('data')
    
    np.save('data/x.npy', x)
    np.save('data/y.npy', y)
    return x, y

if __name__ == '__main__':
    print("Generating test data...")
    x, y = generate_data()
    print(f"Generated {len(x)} samples and saved them in the 'data' directory.") 