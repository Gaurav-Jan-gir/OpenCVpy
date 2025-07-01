import os
import numpy as np

class Load:
    def __init__(self,path=None,logs = None):
        self.data = []
        self.labels = []
        self.path = path
        self.logs = logs
        self.load()
    
    def load(self):
        if self.path is None:
            self.path = os.path.join(os.getcwd(), 'data')
        os.makedirs(self.path,exist_ok=True)
        for filename in os.listdir(self.path):
            if filename.endswith('.npy'):
                path = os.path.join(self.path, filename)
                try:
                    encoding = np.load(path)
                    if isinstance(encoding, np.ndarray) and encoding.shape == (128,):
                        name, id, dno = os.path.splitext(filename)[0].split('_')
                        self.data.append(encoding)
                        self.labels.append((name, id, dno))
                    else:
                        self.logs.append(f"Skipping invalid file (wrong shape): {filename}");
                except Exception as e:
                    self.logs.append(f"Skipping corrupted file: {filename}")

    def append_new_data(self, encoding, name, id, dno):
        if isinstance(encoding, np.ndarray) and encoding.shape == (128,):
            self.data.append(encoding)
            self.labels.append((name, id, dno))
        else:
            self.logs.append("Error: Encoding must be a numpy array with shape (128,)")

    def append_data_in_burst(self, data, labels):
        if len(data) != len(labels):
            self.logs.append("Error: Data and labels must have the same length")
            return
        for encoding, (name, id, dno) in zip(data, labels):
            self.append_new_data(encoding, name, id, dno)