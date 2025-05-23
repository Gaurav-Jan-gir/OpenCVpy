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
                self.data.append(np.load(path))
                name, id = os.path.splitext(filename)[0].split('_')
                self.labels.append((name, id))