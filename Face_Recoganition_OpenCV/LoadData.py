import os
import numpy as np
from interFace_msg import message

class loadData:
    def __init__(self,path=None):
        self.data = []
        self.labels = []
        self.path = path
        self.load()
    
    def load(self):
        # Load all the data from the data directory
        if self.path is None:
            self.path = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(self.path):
            os.makedirs(self.path,exist_ok=True)
        for filename in os.listdir(self.path):
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

    def append_new_data(self, encoding, name, id, dno):
        # Append new data to the data list and labels
        if isinstance(encoding, np.ndarray) and encoding.shape == (128,):
            self.data.append(encoding)
            self.labels.append((name, id, dno))
        else:
            message("Error: Encoding must be a numpy array with shape (128,)")

    def append_data_in_burst(self, data, labels):
        # Append multiple data entries at once
        if len(data) != len(labels):
            message("Error: Data and labels must have the same length")
            return
        for encoding, (name, id, dno) in zip(data, labels):
            self.append_new_data(encoding, name, id, dno)