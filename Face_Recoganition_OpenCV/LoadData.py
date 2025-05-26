import os
import numpy as np

class loadData:
    def __init__(self):
        self.data = []
        self.labels = []
        self.load()
    
    def load(self):
        # Load all the data from the data directory
        for filename in os.listdir(os.path.join(os.getcwd(), 'data')):
            if filename.endswith('.npy'):
                path = os.path.join(os.getcwd(), 'data', filename)
                try:
                    encoding = np.load(path)
                    if isinstance(encoding, np.ndarray) and encoding.shape == (128,):
                        name, id, dno = os.path.splitext(filename)[0].split('_')
                        self.data.append(encoding)
                        self.labels.append((name, id, dno))
                    else:
                        print(f"Skipping invalid file (wrong shape): {filename}")
                except Exception as e:
                    print(f"Skipping corrupted file {filename}: {e}")