import os
import numpy as np
from interFace_msg import message

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
                        message(f"Skipping invalid file (wrong shape): {filename}");
                except Exception as e:
                    message(f"Skipping corrupted file: {filename}")