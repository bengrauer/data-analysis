import pandas as pd
import numpy as np

# Define the number of samples
num_samples = 50

# Generate sample data
data = {
    'id': np.arange(1, num_samples + 1),
    'timestamp': pd.date_range(start='1/1/2020', periods=num_samples, freq='D'),
    'full_sq': np.random.randint(30, 150, size=num_samples),
    'floor': np.random.randint(1, 20, size=num_samples),
    'max_floor': np.random.randint(1, 20, size=num_samples),
    'material': np.random.choice(['brick', 'panel', 'block', 'wood'], size=num_samples),
    'build_year': np.random.randint(1950, 2020, size=num_samples),
    'num_room': np.random.randint(1, 5, size=num_samples),
    'kitch_sq': np.random.randint(5, 30, size=num_samples)
}

# Create DataFrame
df = pd.DataFrame(data)

# Print the sample data
print(df)
df.to_csv('../data/sample.csv', index=False, header=True)