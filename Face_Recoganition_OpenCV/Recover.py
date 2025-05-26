import os
import numpy as np

old_dir = 'data'
new_dir = 'recovered_data'
os.makedirs(new_dir, exist_ok=True)

for file in os.listdir(old_dir):
    if file.endswith('.npy'):
        old_path = os.path.join(old_dir, file)
        new_path = os.path.join(new_dir, file)
        try:
            arr = np.load(old_path, allow_pickle=True)
            # Only save if it's a valid face encoding
            if isinstance(arr, np.ndarray) and arr.shape == (128,):
                np.save(new_path, arr)
                print(f"Recovered: {file}")
            else:
                print(f"Invalid shape, skipping: {file}")
        except Exception as e:
            print(f"Failed to recover {file}: {e}")
